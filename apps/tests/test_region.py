import pytest
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from apps.models import Region


@pytest.fixture(scope="module")
def api_client():
    return APIClient()


@pytest.fixture
def region():
    region = Region.objects.create(name='Toshkent')
    return region


@pytest.mark.django_db
def test_create_region(api_client):
    data = {
        'name': 'Toshkent'
    }

    url = reverse_lazy('region-list')
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    region = Region.objects.first()
    assert region is not None
    assert region.name == data['name']


@pytest.mark.django_db
def test_list_region(region, api_client):
    url = reverse_lazy('region-list')
    response = api_client.get(url)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['count'] == Region.objects.count()


@pytest.mark.django_db
def test_detail_region(region, api_client):
    url = reverse_lazy('region-detail', args=(region.pk,))
    response = api_client.get(url)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data['name'] == region.name


@pytest.mark.django_db
def test_update_region(region, api_client):
    data = {
        'name': 'Botirjon'
    }
    url = reverse_lazy('region-detail', args=(region.pk,))
    response = api_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert data['name'] == response.json()['name']


@pytest.mark.django_db
def test_destroy_region(region, api_client):
    url = reverse_lazy('region-detail', args=(region.pk,))
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Region.objects.exists()
