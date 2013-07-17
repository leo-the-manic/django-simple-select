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


def query(filter_func, terms, queries, query_factory, query_joiner):
    """Use the given terms and `Django queries`_ to filter results.

    :param filter_func: A Django object manager or QuerySet. For example,
                        ``MyModel.objects.filter``.

    :param terms: a sequence of strings to use with the given queries.

    :param queries: a sequence of `Django queries`_ to send to ``filter_func``

    :param query_factory: A callable with the same contract as the Django
                          `Q object`_ constructor.

    :param query_joiner: A callable which takes a sequence of query objects
                         returned from ``query_factory``, and produces a
                         sequence of args to be given to a ``filter_func``

    """
    kwargs = {queries[0]: terms[0]}
    query_factory(**kwargs)


def autocomplete_filter(request):
    from demo import models
    companies = [{'pk': c.pk, 'label': c.name} for c in
                 models.Company.objects.all()]
    return JSONResponse(companies)
