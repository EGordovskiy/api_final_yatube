from rest_framework import serializers
from .models import Post, Comment, Group, Follow, User
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    group = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
        )

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        )
    post_id = serializers.ReadOnlyField()

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Follow
