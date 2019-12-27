from urllib.request import urlopen
import json
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from socnet.serializers import UserSerializer, PostSerializer
from socnet.models import Post
from socnet.permissions import IsAuthorOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format)
    })


@api_view(['GET', 'POST'])
def like_post(request, *args, **kwargs):
    verify_email(1)
    status = False
    if request.user.id is None:
        return Response({
            'status': status
        })
    try:
        post = Post.objects.get(pk=kwargs['pk'])
        status = post.votes.up(request.user.id)
    except Exception as e:
        # TODO: add log
        print(e)
        status = False
    return Response({
        'status': status
    })


@api_view(['GET', 'POST'])
def unlike_post(request, *args, **kwargs):
    status = False
    if request.user.id is None:
        return Response({
            'status': status
        })
    try:
        post = Post.objects.get(pk=kwargs['pk'])
        status = post.votes.down(request.user.id)
    except Exception as e:
        # TODO: add log
        print(e)
        status = False
    return Response({
        'status': status
    })


def verify_email(user_id):
    user_id = 2  # todo: delete on production
    api_key = 'secret'  # todo: get correct api_key
    try:
        user = User.objects.get(id=user_id)
        user_email = user.email
        if user_email:
            with urlopen(
                    f"https://api.hunter.io/v2/email-verifier?email={user_email}&api_key={api_key}") as response:
                response_content = response.read()
            json_response = json.loads(response_content)
            print(json_response)
    except Exception as e:
        # TODO: add log
        print(e)
        json_response = json.loads("{status: 'failed'}")
    return json_response


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
