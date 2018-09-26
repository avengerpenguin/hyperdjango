import json
import pytest
from .models import Person


@pytest.mark.django_db
def test_404(client):
    response = client.get('/notreal')
    print(response)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get(client):
    me = Person(name='Ross')
    me.save()
    response = client.get('/people/1')
    assert response.status_code == 200
    assert json.loads(response.content)['name'] == 'Ross'


@pytest.mark.django_db
def test_put(client):
    me = Person(name='Ross')
    me.save()
    response = client.get('/people/1')
    assert response.status_code == 200
    assert json.loads(response.content)['name'] == 'Ross'

    response = client.put('/people/1', data=json.dumps({
        '@context': {
            '@vocab': 'http://testserver/', '@base': 'http://testserver'
        },
        '@id': '/people/1',
        '@type': 'Person',
        'name': 'Ron'
    }), content_type='application/ld+json')

    assert response.status_code == 200
    assert json.loads(response.content)['name'] == 'Ron'
