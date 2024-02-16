import unittest
import asyncio

from data.yahoo_finance import fetch_stock_data, top_five_day_over_day

class FinanceAPITest(unittest.TestCase):

    def test_yahoo_finance_api_access(self):
        #Usage: tests accessing Yahoo finance api
        result = asyncio.run(fetch_stock_data('AAPL'))
        self.assertTrue(result['connected_to_yahoo_finance'])
        self.assertIsNotNone(result['response'])


    def test_parsing_json_loaded_from_file(self):
        #Usage: tests parsing json
        result = top_five_day_over_day('AAPL', '3mo')
        self.assertTrue(result['json_parsed'])

    def test_calculating_day_over_day_percent_move(self):
        #Usage: tests calculating day over day percent move;
        result = top_five_day_over_day('AAPL', '3mo')
        self.assertIsInstance(result['top_five_changes'], list)
        self.assertEqual(len(result['top_five_changes']), 5)


if __name__ == "__main__":
    unittest.main()