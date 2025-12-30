from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('posts/', PostViewSet, basename='posts')
router.register('comments/', CommentViewSet, basename='comments')
router.register('feed/', PostViewSet, basename='feed')

urlpatterns = router.urls

urlpatterns = [
    path('posts/<int:pk>/like/', include(router.urls)),
    path('posts/<int:pk>/unlike/', include(router.urls)),
]
