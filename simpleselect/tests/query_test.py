import unittest

import mock

from .. import views


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
    """Tests for the create_queries function.

    .. note:: Many of these tests use assertEquals. This is because these are
              MagicMock objects. Django Q objects do *NOT* have a well-defined
              __eq__ method, so if these were integration tests, they would
              all fail (even if the method logic was correct).

    """

    def test_basic_query_constructor_call(self):
        """The query constructor is given the query and a term."""
        Q = mock.MagicMock()
        queries = views.create_queries(['Joe'], ['name__icontains'], Q)
        self.assertEquals(tuple(queries)[0], Q(name__icontains='Joe'))

        Q = mock.MagicMock()
        queries = views.create_queries(['Ma'], ['address__contains'], Q)
        self.assertEquals(tuple(queries)[0], Q(address__contains='Ma'))

    def test_terms_sent_to_all(self):
        """A term is sent to all queries."""
        Q = mock.MagicMock()

        # generators are lazy; tuple() is used to force it to make all objects
        result = tuple(views.create_queries(['Joe'], ['first_name__icontains',
                                                      'last_name__icontains'],
                                            Q))

        expected = [mock.call(first_name__icontains='Joe'),
                    mock.call(last_name__icontains='Joe')]
        self.assertEquals(expected, Q.call_args_list)
        self.assertEquals(len(result), 2)

    def test_all_terms_sent(self):
        """All terms are sent to each query."""
        Q = mock.MagicMock()

        # generators are lazy; tuple() is used to force all objects to be made
        result = tuple(views.create_queries(['John', 'Smith'], ['a__is'], Q))
        expected = [mock.call(a__is='John'), mock.call(a__is='Smith')]
        self.assertEquals(expected, Q.call_args_list)
        self.assertEquals(len(result), 2)


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
        self.assertEquals(views.and_together((q1, q2)), q1 & q2)


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
