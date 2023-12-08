import os
from io import StringIO
from breeze_email_reports.table_format import (_HTMLFormatter, ColSpec,
                                               _splitval, _TextFormatter,
                                               _CSVFormatter, _escape_html_value)
import unittest

TEST_DIR = os.path.join(os.path.split(__file__)[0], 'split_test_files')
# TEST_FILES_DIR = os.path.join(TEST_DIR, 'test_files')
EXPECT_TEXT_FILE = os.path.join(TEST_DIR, 'ExpectedTableText.txt')
EXPECT_HTML_FILE = os.path.join(TEST_DIR, 'ExpectedTableHTML.html')
EXPECT_CSV_FILE = os.path.join(TEST_DIR, 'ExpectedTableCSV.csv')


class TestSplitVal(unittest.TestCase):
    def test_html_escape(self):
        val = ['a;&b', '#z', '<']
        ret = _escape_html_value(val)
        self.assertEqual('a<br/>&amp;b<br/>#z<br/>&lt;', ret)
        ret = _escape_html_value('& <')
        self.assertEqual(ret, '&amp; &lt;')

    def test_splitVal(self):
        # c0_width = 15
        # c1_width = 20
        # c1_width = 10
        # cs0 = ColSpec('c0', width=15)
        # cs1 = ColSpec('c1', width=20)
        cs2 = ColSpec('c2', width=10)

        v0 = 'abcdefghij'
        s0, s1 = _splitval(v0, cs2)
        self.assertEqual(s0, v0)
        self.assertEqual(s1, '')
        s0, s1 = _splitval(v0 + 'xy', cs2)
        self.assertEqual(s0, v0)
        self.assertEqual(s1, 'xy')

        v1 = 'abcd:ef ghij'
        s0, s1 = _splitval(v1, cs2)
        self.assertEqual(s0, 'abcd:')
        self.assertEqual(s1, 'ef ghij')

        s0, s1 = _splitval(v1, cs2, splits=' ')
        self.assertEqual(s0, 'abcd:ef')
        self.assertEqual(s1, 'ghij')


class TestFormatters(unittest.TestCase):
    def setUp(self):
        self.cs0 = ColSpec('c0', width=30)
        self.cs1 = ColSpec('c1', width=20)
        self.cs2 = ColSpec('c2', width=20)
        self.col_specs = [self.cs0, self.cs1, self.cs2]
        self.data = [('aname',
                      [
                        [
                            'afield',
                            'oldval',
                            'newval'
                        ],
                        [
                            'notherfield:withbreak',
                            None,
                            ['new1', 'new2 with a long value']
                        ]
                      ]
                     )
                    ]

    def test_text_format(self):
        formatter = _TextFormatter(self.col_specs)

        out = StringIO()
        formatter.format_table(self.data, out)
        out.seek(0)
        result = out.read()
        # with open(EXPECT_TEXT_FILE, 'w', newline='') as f:
        #     f.write(result)
        with open(EXPECT_TEXT_FILE, 'r', newline='') as f:
            expect = f.read()
        self.assertEqual(expect, result)

    def test_html_format(self):

        formatter = _HTMLFormatter(self.col_specs)

        out = StringIO()
        formatter.format_table(self.data, out)
        out.seek(0)
        result = out.read()
        # with open(EXPECT_HTML_FILE, 'w', newline='') as f:
        #     f.write(result)
        with open(EXPECT_HTML_FILE, 'r', newline='') as f:
            expect = f.read()
        self.assertEqual(expect, result)

    def test_csv_format(self):
        formatter = _CSVFormatter(self.col_specs)

        out = StringIO()
        formatter.format_table(self.data, out)
        out.seek(0)
        result = out.read()
        # with open(EXPECT_CSV_FILE, 'w', newline='') as f:
        #     f.write(result)
        with open(EXPECT_CSV_FILE, 'r', newline='') as f:
            expect = f.read()
        self.assertEqual(expect, result)

