from django.urls import path, include
# from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from socnet import views

urlpatterns = [
    path('', views.api_root),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('posts/<int:pk>/unlike/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth_token/', include('djoser.urls.authtoken')),
]