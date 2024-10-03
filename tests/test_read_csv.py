# tests/test_read_csv.py

import unittest
from src.archer_formatter.read_csv import read_file

class TestReadCSV(unittest.TestCase):
    def test_read_valid_file(self):
        df = read_file('data/base.csv')
        self.assertIsNotNone(df)

    def test_read_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            read_file('data/nonexistent.csv')

if __name__ == '__main__':
    unittest.main()