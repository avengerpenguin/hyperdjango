from importlib import import_module
import yarl
import django
import rdflib
from collections import defaultdict
from rdflib import Graph, URIRef, RDF, Namespace


class LoggingMixIn(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr):
            print('Called: {}'.format(attr))
        return attr


class HyperdjangoStore(rdflib.store.Store, LoggingMixIn):

    models = None

    def open(self, configuration, _):
        if configuration:
            self.models = import_module(configuration)

    def triples(self, t, context=None):
        base = Namespace(context.identifier)
        s, p, o = t
        if not s:
            raise Exception('Inefficient')
        else:
            model_id = self._get_model(s)
            if model_id:
                model, pk = model_id
                try:
                    obj = model.objects.get(pk=pk)
                except model.DoesNotExist:
                    return []

                uri = URIRef(yarl.URL(s).path)
                yield (uri, rdflib.RDF.type, base['/' + model.__name__]), None

                for prop in obj.__dict__:
                    if prop not in ['_state', 'id']:
                        yield (uri, base['/' + prop],
                               rdflib.Literal(getattr(obj, prop))), None

    def addN(self, quads):
        data = defaultdict(dict)
        
        for s, p, o, _ in quads:
            print(s, p, o)
            data[s][p] = o

        for s in data:
            model_id = self._get_model(s)
            if model_id:
                model, pk = model_id
                try:
                    obj = model.objects.get(pk=pk)
                except model.DoesNotExist:
                    obj = model(pk=pk)

                for p, o in data[s].items():
                    prop = p.split('/')[-1]
                    setattr(obj, prop, o.toPython())

                obj.save()

    def remove(self, t, context=None):
        s, p, o = t
        if not s:
            raise Exception('Inefficient')
        else:
            model_id = self._get_model(s)
            if model_id:
                model, pk = model_id
                try:
                    obj = model.objects.get(pk=pk)
                except model.DoesNotExist:
                    return

                if True or p == RDF.type:
                    obj.delete()
                else:
                    raise NotImplementedError

    def _get_model(self, s):
        path = yarl.URL(s).path
        for n in dir(self.models):
            model = getattr(self.models, n)
            if isinstance(model, django.db.models.base.ModelBase):
                if model.uri_pattern:
                    match = model.uri_pattern.match(path)
                    if match:
                        return model, match.group(1)
