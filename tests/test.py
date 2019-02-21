import pytest
from . import app
from .models import Thing


@pytest.mark.django_db
def test(client):
    thing = Thing(name='Berlin')
    thing.save()

    r = client.get('/things/1')

    assert r.status_code == 200
