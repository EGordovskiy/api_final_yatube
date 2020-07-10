from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from .models import Post, User, Comment, Follow, Group
from rest_framework import viewsets, permissions, filters
from .serializers import (
    CommentSerializer, FollowSerializer,
    GroupSerializer, PostSerializer, UserSerializer
)
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly, IsProfileAuthorOrReadOnly
from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head']
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        get_object_or_404(User, username=self.request.user)
        following = User.objects.get(
            username=self.request.data.get('following'))
        user = self.request.user
        exist = Follow.objects.filter(
            user=user, following=following
        ).exists()

        if exist:
            raise ValidationError('You are already subscribed.')

        if following != user:
            serializer.save(user=user, following=following)
        else:
            raise ValidationError("You can't subscribe to yourself.")


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['=group__title']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileAuthorOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user)
