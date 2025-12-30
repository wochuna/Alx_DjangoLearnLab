from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    model = Post
    fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    model = Comment
    fields = '__all__'    
    