from django.test import TestCase
from django.db import connection
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from socnet.models import Post


class TestPostListAPIView(APITestCase):
    post_list_url = reverse('post-list')
    user_list_url = reverse('user-list')

    def test_post_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.post_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)