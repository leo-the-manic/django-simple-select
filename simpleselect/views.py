# Create your views here.
import json
from functools import reduce

import django.db.models
import django.http

from . import fields


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


def and_together(queries):
    """Join the given queries by ANDing.

    :type  queries: iterable
    :param queries: All involved Query objects.

    If ``queries`` is empty, this will raise a TypeError.

    """
    return reduce(lambda a, b: a & b, queries)


def or_together(queries):
    """Join the given queries together by ORing.

    This means::

        or_together(Q(foo='bar'), Q(fizz='buzz'))

    is identical to::

        Q(foo='bar') | Q(fizz='buzz')


    :type  queries: seq of Query object
    :param queries: Isolated Query objects (e.g. Django `Q objects`_)

    :return: A single Query that is all ``queries`` OR'd together.

    .. note:: if queries is empty, this will raise a TypeError

    """
    return reduce(lambda a, b: a | b, queries)


def create_queries(terms, queries, query_factory):
    """Make a sequence of query objects out of terms and query strings.

    Although "query objects" are assumed to be Django `Q objects`_, you can
    use ``query_factory`` to supply whatever you like.

    This does a "cartesian product"; in other words, this call::

        tuple(create_queries(['John', 'Smith'],
                             ['first_name__icontains, last_name__icontains'],
                             Q))

    will be logically equivalent to this::

        (Q(first_name__icontains='John'), Q(first_name__icontains='Smith'),
         Q(last_name__icontains='John'), Q(last_name__icontains='Smith'))

    .. note:: The *ordering* is not guaranteed, but the elements of both tuples
              will be equivalent.

    :type  terms: seq of str
    :param terms: Search terms to query with, e.g. ["John", "Smith"]

    :type  queries: seq of str
    :param queries: Django query strings, e.g. ["name__icontains"]

    :type  query_factory: callable
    :param query_factory: A callable with the same contract as Django's
                          `Q object`_ constructor. In most cases you will
                          simply use ``django.db.models.Q`` here.

    :return: A generator which yields query objects.

    >>> from django.db.models import Q
    >>> queries_are_equal = lambda a, b: a.children == b.children
    >>>
    >>> queries = create_queries(['Joe'], ['name__contains'], Q)
    >>> a = tuple(queries)[0]
    >>> b = Q(name__contains='Joe')
    >>> queries_are_equal(a, b)
    True

    """
    Q = query_factory
    for term in terms:
        term_on_all_queries = (Q(**{query: term}) for query in queries)
        yield or_together(term_on_all_queries)


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
                                  ``query_factory``. :py:func:`create_queries`
                                  is a provided applier you can use.

    :param query_joiner: A callable which takes a sequence of query objects
                         returned from ``query_factory``, and produces a
                         single query object to be given to a ``filter_func``

    """
    query_objects = query_factory_applier(terms, queries, query_factory)
    final_query = query_joiner(query_objects)
    return filter_func(final_query)


def jsonify_queryset(qset):
    """Get a JSONResponse which is a list of objects in qset.

    qset can actually be any iterable.

    """
    objs = [{'pk': o.pk, 'label': str(o)} for o in qset]
    return JSONResponse(objs)


def do_search(field, request):
    """Process an autosuggestion search."""
    objects = query(field.data.filter,
                    request.GET.get('term', '').split(),
                    field.queries,
                    django.db.models.Q,
                    create_queries,
                    and_together)
    return jsonify_queryset(objects)


def get_item_detail(field, request):
    """Process a request for one specific object by it's ID."""
    id = request.GET['id']
    obj = field.data.get(pk=id)
    return jsonify_queryset([obj])


def autocomplete_filter(request):
    field = request.GET.get('field')
    if field not in fields.REGISTRY:
        raise django.http.Http404("Can't find field {} in global registry."
                                  "Registered fields: {}"
                                  .format(field, fields.REGISTRY.keys()))
    field = fields.REGISTRY[request.GET['field']]

    # this is either an autosuggest search, or a query for a specific item
    # by its ID for its autocomplete data
    if request.GET.get('id'):
        delegate = get_item_detail
    else:
        delegate = do_search

    return delegate(field, request)
