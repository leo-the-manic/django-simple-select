import unittest

import mock

from . import views


class JSONResponseTest(unittest.TestCase):
    """Tests for the JSONResponse class."""

    def test_sets_content_type(self):
        """JSON responses have a header 'content-type: application/json'"""
        resp = views.JSONResponse()
        self.assertEquals(resp['content-type'], 'application/json')

    def test_converts_to_json(self):
        """JSON responses convert their content to JSON."""
        json = mock.MagicMock(return_value='bar')
        resp = views.JSONResponse(content='foo', json_service=json)
        json.assert_called_with('foo')
        self.assertEquals(resp.content, 'bar')

        json = mock.MagicMock(return_value='buzz')
        resp = views.JSONResponse(content='fizz', json_service=json)
        json.assert_called_with('fizz')
        self.assertEquals(resp.content, 'buzz')


class CreateQueriesTest(unittest.TestCase):
    """Tests for the create_queries function."""

    def test_basic_query_constructor_call(self):
        """The query constructor is given the query and a term."""
        Q = mock.MagicMock()
        views.create_queries(['Joe'], ['name__icontains'], Q)
        Q.assert_called_with(name__icontains='Joe')

        Q = mock.MagicMock()
        views.create_queries(['Ma'], ['address__contains'], Q)
        Q.assert_called_with(address__contains='Ma')

    def test_multiple_queries_get_terms(self):
        """Each query gets called with a term."""
        Q = mock.MagicMock()
        views.create_queries(['Joe'],
                             ['first_name__icontains', 'last_name__icontains'],
                             Q)


class QueryTest(unittest.TestCase):
    """Tests for the query() function."""

    def test_query_joiner_used(self):
        """All independent query objects are joined by query_joiner."""
        datasource = mock.MagicMock()
        applier = mock.MagicMock()
        joiner = mock.MagicMock()
        Q = mock.MagicMock()

        views.query(datasource, ['Joe'], ['name__contains'], Q, applier,
                    joiner)
        pos_args = joiner.call_args[0]
        queryseq = pos_args[0]
        self.assertEquals(queryseq, applier.return_value)
