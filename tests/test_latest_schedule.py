import importlib.util
import unittest
from datetime import date
from pathlib import Path

spec = importlib.util.spec_from_file_location('fetch_latest', Path(__file__).parents[1] / 'scripts/fetch_latest.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LatestTests(unittest.TestCase):
    def test_uses_korean_publication_date_and_rejects_future_or_foreign_urls(self):
        def item(url, timestamp):
            return {'canonical_url': url, 'display_date': timestamp}
        source = '/national/nie/chinese/2026/11/16/PUBLISHER_ID/'
        items = [item(source, '2026-11-15T15:00:00Z'),
                 item('/national/nie/chinese/future/', '2026-11-16T15:00:00Z'),
                 item('https://other.example/national/nie/chinese/id', '2026-11-16T01:00:00Z')]
        self.assertEqual(module.latest(items, date(2026, 11, 16)), module.ROOT + source)

    def test_no_source_is_not_invented(self):
        with self.assertRaises(ValueError):
            module.latest([], date(2026, 11, 16))
