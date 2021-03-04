import django
import inflect
import pytest
from hypothesis import assume, given, strategies
from laconia import ThingFactory
from rdflib import Graph, Namespace

from .models import Thing

p = inflect.engine()


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
    return strategies.from_regex(model_class.uri_pattern().match)


def entity_from_response(r, rel_path):
    g = Graph()
    g.bind("test", Namespace("http://testserver/"))
    g.parse(data=r.content, format=r["Content-Type"])

    assert len(g) > 0

    entity = ThingFactory(g)(Namespace("http://testserver/")[rel_path])

    return entity


@given(models(Thing))
@pytest.mark.django_db
def test_getting_object(client, thing):
    # Don't test for things with blank names just now
    assume(thing.name)

    r = client.get(f"/things/{thing.pk}")
    assert r.status_code == 200

    entity = entity_from_response(r, f"things/{thing.pk}")
    assert {
        thing.name,
    } == set(entity.test_name)


@pytest.mark.django_db
@given(entities(Thing))
def test_putting_new_entity(client, uri):
    r = client.put(uri)
    assert r.status_code == 201
