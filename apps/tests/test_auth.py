from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
import pytest
from .test_region import api_client

@pytest.fixture
def user_client():
    user = User.objects.create_user(username='john', email='js@js.com', password='js.sj')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.mark.django_db
def test_base_view(user_client):
    url = reverse_lazy('base_view')
    response = user_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['msg'] == 'hello world'


@pytest.mark.django_db
def test_base_view(api_client):
    url = reverse_lazy('base_view')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
