from rest_framework import serializers
from django.contrib.auth.models import User
from socnet.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['url', 'id', 'author', 'title', 'body']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'posts']