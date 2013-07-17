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


class QueryTest(unittest.TestCase):
    """Tests for the query() function."""

    def test_basic_query_constructor_call(self):
        """The query constructor is given a filter and a terms."""
        datasource = mock.MagicMock()
        joiner = mock.MagicMock()

        Q = mock.MagicMock()
        views.query(datasource, ['Joe'], ['name__icontains'], Q, joiner)
        Q.assert_called_with(name__icontains='Joe')

        Q = mock.MagicMock()
        views.query(datasource, ['Ma'], ['address__contains'], Q, joiner)
        Q.assert_called_with(address__contains='Ma')
