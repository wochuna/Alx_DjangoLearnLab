from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        


        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                post=post,
                notification_type='like'
            )
            return Response({'message': 'post liked'},
                            status=status.HTTP_201_CREATED
                            )
        
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
             
        if like:
            like.delete()
            return Response({'status': 'post unliked'}
                            , status=status.HTTP_200_OK
                            )
        return Response({'message': 'Not liked yet'},
                        status=status.HTTP_400_BAD_REQUEST
        )


class FeedViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(feed_posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
