import unittest
from unittest import mock

from .. import views


class JSONResponseTest(unittest.TestCase):
    """Tests for the JSONResponse class."""

    def test_sets_content_type(self):
        """JSON responses have a header 'content-type: application/json'"""
        resp = views.JSONResponse()
        self.assertEqual(resp['content-type'], 'application/json')

    def test_converts_to_json(self):
        """JSON responses convert their content to JSON."""
        json = mock.MagicMock(return_value='bar')
        resp = views.JSONResponse(content='foo', json_converter=json)
        json.assert_called_with('foo')
        self.assertEqual(resp.content, b'bar')

        json = mock.MagicMock(return_value='buzz')
        resp = views.JSONResponse(content='fizz', json_converter=json)
        json.assert_called_with('fizz')
        self.assertEqual(resp.content, b'buzz')


class CreateQueriesTest(unittest.TestCase):
    """Tests for the create_queries function.

    .. note:: Many of these tests use assertEqual. This is because these are
              MagicMock objects. Django Q objects do *NOT* have a well-defined
              __eq__ method, so if these were integration tests, they would
              all fail (even if the method logic was correct).

    """

    def test_basic_query_constructor_call(self):
        """The query constructor is given the query and a term."""

        # TODO: these tests are misleading, testing equality to Q doesn't work
        # right and is always true because of the way mock.MagicMock works
        Q = mock.MagicMock()
        queries = views.create_queries(['Joe'], ['name__icontains'], Q)
        self.assertEqual(tuple(queries)[0], Q(name__icontains='Joe'))

        Q = mock.MagicMock()
        queries = views.create_queries(['Ma'], ['address__contains'], Q)
        self.assertEqual(tuple(queries)[0], Q(address__contains='Ma'))

    # since Q objects can't be checked for equality I'm not sure how to
    # properly unit test this


class OrTogetherTest(unittest.TestCase):
    """Tests for the or_together() function."""

    def test_single_query_goes_to_empty(self):
        """or_together()'ing one thing pairs with the empty value."""
        empty = mock.MagicMock()
        q1 = mock.MagicMock()
        self.assertEqual(views.or_together((q1,)), q1)

    def test_multiple_queries_combined(self):
        """or_goether()'ing two things pairs both with the empty value."""
        empty = mock.MagicMock()
        q1, q2 = mock.MagicMock(), mock.MagicMock()
        self.assertEqual(views.or_together((q1, q2)),
                          q1 | q2)


class AndTogetherTest(unittest.TestCase):
    """Tests for the and_together() function."""

    def test_single_query_gets_returned(self):
        """and_together()'ing a single query returns that query."""
        q1 = mock.MagicMock()
        self.assertIs(views.and_together((q1,)), q1)

    def test_multiple_queries_anded_together(self):
        """and_together() on many queries uses the & operator to combine."""
        q1 = mock.MagicMock()
        q2 = mock.MagicMock()
        self.assertEqual(views.and_together((q1, q2)), q1 & q2)


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
        self.assertEqual(self.result, self.datasource.return_value)

    def test_filter_gets_joined_query_objects(self):
        """filter_func is given the result of query_factory_joiner."""
        self.datasource.assert_called_with(self.joiner.return_value)

    def test_factory_applier_used(self):
        """query_factory_applier is given the appropriate arguments"""
        self.applier.assert_called_with(['sample_term'], ['sample_query'],
                                        self.Q)
