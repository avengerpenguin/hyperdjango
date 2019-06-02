import pytest
from rdflib import Graph, Namespace
from laconia import ThingFactory
from .models import Thing


@pytest.mark.django_db
def test_getting_object(client):
    thing = Thing(name='Berlin')
    thing.save()

    r = client.get('/things/1')

    assert r.status_code == 200
    g = Graph()
    g.bind('test', Namespace('http://testserver/'))
    g.parse(data=r.content, format=r['Content-Type'])
    entity = ThingFactory(g)(Namespace('http://testserver/')['things/1'])

    assert 'Berlin' in entity.test_name


@pytest.mark.django_db
def test_object_changing_in_backend(client):
    thing = Thing(name='Giraffe')
    thing.save()

    r = client.get('/things/1')

    assert r.status_code == 200
    g = Graph()
    g.bind('test', Namespace('http://testserver/'))
    g.parse(data=r.content, format=r['Content-Type'])
    entity = ThingFactory(g)(Namespace('http://testserver/')['things/1'])

    assert 'Giraffe' in entity.test_name

    thing.name = 'Elephant'
    thing.save()

    r = client.get('/things/1')

    assert r.status_code == 200
    g = Graph()
    g.bind('test', Namespace('http://testserver/'))
    g.parse(data=r.content, format=r['Content-Type'])
    entity = ThingFactory(g)(Namespace('http://testserver/')['things/1'])

    assert 'Elephant' in set(entity.test_name)
