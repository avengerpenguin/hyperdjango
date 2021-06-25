import json
import sys

from django.http import HttpRequest, HttpResponse
from django.views.generic.base import View
from flask_rdf.format import FormatSelector
from pyld import jsonld
from rdflib import Graph, URIRef
from rdflib.plugin import register
from rdflib.store import Store

FORMAT = FormatSelector()
FORMAT.add_format("application/ld+json", "json-ld")
FORMAT.default_mimetype = "application/ld+json"
FORMAT.wildcard_mimetype = "application/ld+json"


register("Hyperdjango", Store, "hyperdjango.store", "HyperdjangoStore")


class HyperView(View):

    models = sys.modules[__name__]

    def get(self, request, *args, **kwargs):

        base_url = "http://" + request.get_host()

        graph = Graph("Hyperdjango", identifier=URIRef(base_url))
        graph.open(configuration=self.models.__name__)

        r = graph.query(
            """
        PREFIX schema: <http://schema.org/>
        CONSTRUCT
        WHERE {
            ?x ?p ?y .
        }
        """,
            initBindings={"x": URIRef(base_url + request.path)},
        )

        if len(r) == 0:
            return HttpResponse(status=404)

        g = Graph()

        for r_ in r:
            g.add(r_)

        mimetype, rdf_format = FORMAT.decide(
            request.META.get("HTTP_ACCEPT", "application/ld+json"),
            g.context_aware,
        )

        body = g.serialize(format=rdf_format, publicID=base_url).decode("utf8")

        if rdf_format == "json-ld":
            body = json.dumps(
                jsonld.compact(
                    jsonld.frame(
                        json.loads(body),
                        {"@id": base_url + request.path},
                        {
                            "base": base_url,
                        },
                    ),
                    {
                        "@vocab": base_url + "/",
                        "@base": base_url,
                    },
                )
            )

        return HttpResponse(body, content_type=mimetype)

    def put(self, request: HttpRequest, *args, **kwargs):
        if not request.content_type:
            return HttpResponse(status=415)

        base_url = "http://" + request.get_host()

        update_graph = Graph()
        update_graph.parse(data=request.body, format=request.content_type)

        graph = Graph("Hyperdjango", identifier=URIRef(base_url))
        graph.open(configuration=self.models.__name__)

        graph.update(
            """
        DELETE { ?x ?p ?y }
        WHERE {
            ?x ?p ?y .
        }
        """,
            initBindings={"x": URIRef(base_url + request.path)},
        )

        graph.update(
            """
        INSERT DATA {
        """
            + update_graph.serialize(format="nt").decode("utf8")
            + """
        }
        """,
            initBindings={"x": URIRef(base_url + request.path)},
        )

        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        base_url = "http://" + request.get_host()

        graph = Graph("Hyperdjango", identifier=URIRef(base_url))
        graph.open(configuration=self.models.__name__)

        graph.update(
            """
        DELETE { ?x ?p ?y }
        WHERE {
            ?x ?p ?y .
        }
        """,
            initBindings={"x": URIRef(base_url + request.path)},
        )

        return HttpResponse(status=201)
