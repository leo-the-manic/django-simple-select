# Create your views here.
import json

import django.db.models
import django.http


class JSONResponse(django.http.HttpResponse):
    """An HTTP response with a 'content-type: application/json' header"""

    def __init__(self, content='', status=200, reason=None,
                 json_converter=json.dumps):
        """Create a JSONResponse by converting the given content to JSON.

        :type  content: Python object
        :param content: The response body, which gets converted to JSON.

        :type  json_converter: callable
        :param json_converter: A Python->JSON converter. By default, this is
                               the ``json.dumps`` function of the Python
                               standard library.

        For all other parameters, see the `official Django documentation`_.

        .. _official Django documentation: https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpResponse.__init__

        """
        json_content = json_converter(content)
        super(JSONResponse, self).__init__(json_content, 'application/json',
                                           status, reason)


def or_together(queries, empty_val=django.db.models.Q()):
    """Join the given queries together by ORing.

    This means::

        or_together(Q(foo='bar'), Q(fizz='buzz'))

    is identical to::

        Q(foo='bar') | Q(fizz='buzz')


    :type  queries: seq of Query object
    :param queries: Isolated Query objects (e.g. Django `Q objects`_)

    :type  empty_val: Query object
    :param empty_val: An empty query safe for OR-ing with anything without
                      changing the meaning of the query. E.g. ``Q()``

    :return: A single Query that is all ``queries`` OR'd together.

    """
    return reduce(lambda a, b: a | b, queries, empty_val)


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
    >>> queries_are_equal = lambda a, b: a.children == b.children
    >>>
    >>> a = create_queries(['Joe'], ['name__contains'], Q)
    >>> b = Q(name__contains='Joe')
    >>> queries_are_equal(a[0], b)
    True

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
                         single query object to be given to a ``filter_func``

    """
    query_objects = query_factory_applier(terms, queries, query_factory)
    final_query = query_joiner(query_objects)
    return filter_func(final_query)


def autocomplete_filter(request):
    from demo import models
    companies = [{'pk': c.pk, 'label': c.name} for c in
                 models.Company.objects.all()]
    return JSONResponse(companies)
