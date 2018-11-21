import os, sys
from unittest import TestCase
from converters import bankinter_parser, visa_parser, personal_parser, business_parser

class TestParsers(TestCase):

    def test_bankinter(self):
        res = bankinter_parser.parse(os.path.join(sys.path[0], 'tests', 'files', 'bankinter.xls'))
        self.assertIs(len(res), 4)

    def test_visa(self):
        res = visa_parser.parse(os.path.join(sys.path[0], 'tests', 'files', 'visa.xls'))
        self.assertIs(len(res), 3)
    
    def test_personal(self):
        res = personal_parser.parse(os.path.join(sys.path[0], 'tests', 'files', 'personal.xls'))
        self.assertIs(len(res), 3)
    
    def test_business(self):
        res = business_parser.parse(os.path.join(sys.path[0], 'tests', 'files', 'business.csv'))
        self.assertIs(len(res), 2)
