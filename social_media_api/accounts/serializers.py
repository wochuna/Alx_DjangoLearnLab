from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model().objects.create_user

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    verify_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','username','email','password','role')
    
    def validate(self, data):
        if data['password'] != data['verify_password']:
          raise serializers.ValidationError("Passwords must match!")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('verify_password')
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
