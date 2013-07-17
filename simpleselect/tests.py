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
        resp = views.JSONResponse(content='foo', json_converter=json)
        json.assert_called_with('foo')
        self.assertEquals(resp.content, 'bar')

        json = mock.MagicMock(return_value='buzz')
        resp = views.JSONResponse(content='fizz', json_converter=json)
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


class OrTogetherTest(unittest.TestCase):
    """Tests for the or_together() function."""

    def test_single_query_goes_to_empty(self):
        """or_together()'ing one thing pairs with the empty value."""
        empty = mock.MagicMock()
        q1 = mock.MagicMock()
        self.assertEquals(views.or_together((q1,), empty), empty | q1)

    def test_multiple_queries_combined(self):
        """or_goether()'ing two things pairs both with the empty value."""
        empty = mock.MagicMock()
        q1, q2 = mock.MagicMock(), mock.MagicMock()
        self.assertEquals(views.or_together((q1, q2), empty),
                          empty | q1 | q2)


class QueryTest(unittest.TestCase):
    """Tests for the query() function."""

    def setUp(self):
        """Mock a call to query(), and all dependcies.

        Creates mock objects and stores them in self.datasource, self.applier,
        self.joiner, and self.Q.

        These correspond to filter_func, query_factory_applier, query_joiner,
        and query_factory.

        """
        self.Q = mock.MagicMock()
        self.applier = mock.MagicMock()
        self.datasource = mock.MagicMock()
        self.joiner = mock.MagicMock()

        self.result = views.query(self.datasource, ['sample_term'],
                                  ['sample_query'], self.Q, self.applier,
                                  self.joiner)

    def test_query_joiner_used(self):
        """All independent query objects are joined by query_joiner."""
        self.joiner.assert_called_with(self.applier.return_value)

    def test_returns_filter_func(self):
        """The value returned from the function is from filter_func."""
        self.assertEquals(self.result, self.datasource.return_value)

    def test_filter_gets_joined_query_objects(self):
        """filter_func is given the result of query_factory_joiner."""
        self.datasource.assert_called_with(self.joiner.return_value)

    def test_factory_applier_used(self):
        """query_factory_applier is given the appropriate arguments"""
        self.applier.assert_called_with(['sample_term'], ['sample_query'],
                                        self.Q)
