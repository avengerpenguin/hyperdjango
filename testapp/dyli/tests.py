import re
import pytest
import httpretty
from rdflib import Graph, Namespace
from .models import Thing
from laconia import ThingFactory


@pytest.fixture(autouse=False, scope='function')
def mock_requests_to_use_django_test_client(request, client):

    def get_callback(http_request, uri, headers):

        httpretty.disable()
        r = client.get(uri, headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        httpretty.enable()
        return int(r.status_code), response_headers, r.data

    def put_callback(http_request, uri, headers):

        httpretty.disable()
        r = client.put(uri,
                       data=http_request.body,
                       headers=dict(http_request.headers))

        response_headers = {
            'content-type': r.headers['Content-Type'],
            'content-length': len(r.headers['Content-Length']),
        }
        response_headers.update(headers)

        httpretty.enable()
        return int(r.status_code), response_headers, r.data

    httpretty.register_uri(httpretty.GET,
                           re.compile('http://example.com/.*'),
                           body=get_callback)
    httpretty.register_uri(httpretty.PUT,
                           re.compile('http://example.com/.*'),
                           body=put_callback)
    httpretty.enable()

    request.addfinalizer(httpretty.disable)
    request.addfinalizer(httpretty.reset)


@pytest.mark.django_db
def test_thing_title(client):
    thing = Thing(name='Berlin')
    thing.save()

    r = client.get('/things/1')

    assert r.status_code == 200

    print(dir(r))
    g = Graph()
    g.bind('test', Namespace('http://testserver/'))
    g.parse(data=r.content, format=r['Content-Type'])
    entity = ThingFactory(g)(Namespace('http://testserver/')['things/1'])

    assert 'Berlin' in set(entity.test_name)
