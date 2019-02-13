import pytest


@pytest.mark.django_db
def test(client):
    assert client.get('/').status_code == 200
