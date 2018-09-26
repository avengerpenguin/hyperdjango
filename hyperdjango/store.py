from importlib import import_module
import yarl
import django
import rdflib
from collections import defaultdict
from rdflib import Variable, Graph, BNode, URIRef, Literal, RDF, Namespace
from rdflib.plugins.sparql import CUSTOM_EVALS
from rdflib.plugins.sparql.sparql import Query, QueryContext
from rdflib.plugins.sparql.parser import parseQuery, parseUpdate
from rdflib.plugins.sparql.algebra import translateQuery, translateUpdate


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

    def open(self, configuration, create):
        if configuration:
            self.models = import_module(configuration)

    def triples(self, t, context=None):
        base = Namespace(context.identifier)
        s, p, o = t
        if not s:
            raise Exception('Inefficient')
        else:
            path = yarl.URL(s).path
            for n in dir(self.models):
                model = getattr(self.models, n)
                if isinstance(model, django.db.models.base.ModelBase):
                    if model.uri_pattern:
                        match = model.uri_pattern.match(path)
                        if match:
                            try:
                                obj = model.objects.get(pk=match.group(1))
                            except model.DoesNotExist:
                                return []
                            
                            g = Graph()
                            uri = URIRef(path)
                            yield (uri, rdflib.RDF.type, base['/' + model.__name__]), None
                            
                            for prop in obj.__dict__:
                                if prop not in ['_state', 'id']:
                                    yield (uri, base['/' + prop], rdflib.Literal(getattr(obj, prop))), None

    def addN(self, quads):
        #print('Quads: {}'.format(list(quads)))

        data = defaultdict(dict)
        
        for s, p, o, _ in quads:
            print(s, p, o)
            data[s][p] = o

        print(dict(data))

        for s in data:
            path = yarl.URL(s).path
            for n in dir(self.models):
                model = getattr(self.models, n)
                if isinstance(model, django.db.models.base.ModelBase):
                    if model.uri_pattern:
                        match = model.uri_pattern.match(path)
                        if match:
                            try:
                                obj = model.objects.get(pk=match.group(1))
                            except model.DoesNotExist:
                                obj = model(pk=match.group(1))

                            for p, o in data[s].items():
                                prop = p.split('/')[-1]
                                setattr(obj, prop, o.toPython())

                            obj.save()
                            print(obj)
                            print(list(model.objects.all())[0].name)
                
            
        
                                    
    def remove(self, t, context=None):
        base = Namespace(context.identifier)
        s, p, o = t
        if not s:
            raise Exception('Inefficient')
        else:
            path = yarl.URL(s).path
            for n in dir(self.models):
                model = getattr(self.models, n)
                if isinstance(model, django.db.models.base.ModelBase):
                    if model.uri_pattern:
                        match = model.uri_pattern.match(path)
                        if match:
                            try:
                                obj = model.objects.get(pk=match.group(1))
                            except model.DoesNotExist:
                                return

                            if True or p == RDF.type:
                                obj.delete()
                            else:
                                raise NotImplementedError
