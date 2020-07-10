from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    CommentViewSet, GroupList,
    FollowViewSet, UserViewSet,
    PostViewSet)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
router.register('follow', FollowViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/group/', GroupList.as_view()),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
