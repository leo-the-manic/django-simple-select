# Create your views here.
import json

import django.http


class JSONResponse(django.http.HttpResponse):
    """An HTTP response with a 'content-type: application/json' header"""

    def __init__(self, content='', status=200, reason=None,
                 json_service=json.dumps):
        """Create a JSONResponse by converting the content to JSON.

        :param content: The Python object to convert to JSON and return.

        :param json_service: A callable which takes a Python object and returns
                             a JSON string. By default, this is the
                             ``json.dumps`` function of the Python standard
                             library.

        For all other parameters, see the `official Django documentation`_.

        .. _official Django documentation: https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse.__init__

        """
        json_content = json_service(content)
        super(JSONResponse, self).__init__(json_content, 'application/json',
                                           status, reason)

def create_queries(terms, queries, query_factory):
    """Make a sequence of query objects out of terms and query strings.

    :type  terms: seq of str
    :param terms: Search terms to query with, e.g. ["John", "Smith"]

    :type  queries: seq of str
    :param queries: Django query strings, e.g. ["name__icontains"]

    :type  query_factory: callable
    :param query_factory: A callable with the same contract as Django's
                          `Q object`_ constructor. In most cases you will
                          simply use ``django.db.models.Q`` here.

    :return: A sequence of query objects.

    >>> from django.db.models import Q
    >>> a = create_queries(['Joe'], ['name__contains'], Q)
    >>> b = Q(name__contains='Joe')
    >>> a[0].children == b.children
    True
    >>> # unfortunately == isn't defined for Q objects; this was the best I
    >>> # could do. But a[0] == b

    """
    # temporary implementation
    kwargs = {queries[0]: terms[0]}
    return (query_factory(**kwargs),)


def query(filter_func, terms, queries, query_factory, query_factory_applier,
          query_joiner):
    """Use the given terms and `Django queries`_ to filter results.

    :param filter_func: A Django object manager or QuerySet. For example,
                        ``MyModel.objects.filter``.

    :param terms: a sequence of strings to use with the given queries.

    :param queries: a sequence of `Django queries`_ to send to ``filter_func``

    :param query_factory: A callable with the same contract as the Django
                          `Q object`_ constructor.

    :param query_factory_applier: A callable which takes a list of terms, a
                                  list of filters, and ``query_factory``, and
                                  returns a sequence of objects produced by
                                  ``query_factory``.

    :param query_joiner: A callable which takes a sequence of query objects
                         returned from ``query_factory``, and produces a
                         sequence of args to be given to a ``filter_func``

    """
    query_objects = query_factory_applier(terms, queries, query_factory)
    query_joiner(query_objects)
    return filter_func()


def autocomplete_filter(request):
    from demo import models
    companies = [{'pk': c.pk, 'label': c.name} for c in
                 models.Company.objects.all()]
    return JSONResponse(companies)
