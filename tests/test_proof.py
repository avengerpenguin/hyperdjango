import django
import inflect
import pytest
from django.test import Client
from hypothesis import assume, given, strategies
from laconia import ThingFactory
from pytest_django.lazy_django import skip_if_no_django
from rdflib import RDF, Graph, Namespace, URIRef

from .models import Thing

p = inflect.engine()


@pytest.fixture(scope="session")
def client():
    """A Django test client instance."""
    skip_if_no_django()

    from django.test.client import Client

    return Client()


def gen_values(f):
    if isinstance(f, django.db.models.CharField):
        return strategies.text()
    else:
        return strategies.none()


def models(model_class):
    def make_model(**kwargs):
        model = model_class(**kwargs)
        model.save()
        return model

    return strategies.builds(
        make_model,
        **{f.name: gen_values(f) for f in model_class._meta.get_fields()},
    )


def entities(model_class):
    return strategies.from_regex(model_class.uri_pattern)


def entity_from_response(r, rel_path):
    g = Graph()
    g.parse(data=r.content, format=r["Content-Type"])
    g.add(
        (
            URIRef("http://testserver/name"),
            RDF.type,
            URIRef("http://www.w3.org/2002/07/owl#FunctionalProperty"),
        )
    )
    g.bind("test", Namespace("http://testserver/"))

    assert len(g) > 0

    entity = ThingFactory(g)(Namespace("http://testserver/")[rel_path])

    return entity


@given(models(Thing))
@pytest.mark.django_db
def test_getting_object(client: Client, thing: Thing):
    # Don't test for things with blank names just now
    assume(thing.name)

    r = client.get(f"/things/{thing.pk}")
    assert r.status_code == 200

    entity = entity_from_response(r, f"things/{thing.pk}")
    assert entity.test_name == thing.name


@given(models(Thing))
@pytest.mark.django_db
def test_putting_new_entity(client: Client, thing: Thing):
    assume(thing.name)

    r = client.get(f"/things/{thing.pk}")
    assert r.status_code == 200

    entity = entity_from_response(r, f"things/{thing.pk}")
    assert entity.test_name == thing.name

    entity.test_name = "changed"

    r = client.put(
        f"/things/{thing.pk}",
        data=entity._store.serialize(format="turtle"),
        content_type="text/turtle",
    )
    assert r.status_code == 200

    r = client.get(f"/things/{thing.pk}")
    assert r.status_code == 200

    entity = entity_from_response(r, f"things/{thing.pk}")
    assert entity.test_name == "changed"
