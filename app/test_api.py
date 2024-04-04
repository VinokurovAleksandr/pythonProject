'''import unittest
from unittest import mock


class Test_insert_rows(unittest.TestCase):

    def fix_dbc(self):
        dbc = mock.MagicMock(spec=['cursor'])
        dbc.autocommit = True
        return dbc

    def fix_rows(self):
        rows = [{'id':1, 'name':'John'},
                {'id':2, 'name':'Jane'},]
        return rows

    def test_insert_rows_calls_cursor_method(self):
        dbc = self.fix_dbc()
        rows = self.fix_rows()
        insert_rows(rows, 'users', dbc)
        self.assertTrue(dbc.cursor.called)

if __name__ == '__main__':
    unittest.main(argv=['', '-v'])'''

