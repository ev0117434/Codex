import unittest

from snapshot.metrics import MetricsRegistry


class TestMetricsRegistry(unittest.TestCase):
    def test_inc_and_snapshot(self):
        metrics = MetricsRegistry()
        metrics.inc("ticks")
        metrics.inc("ticks", 2)
        self.assertEqual(metrics.snapshot()["ticks"], 3)


if __name__ == "__main__":
    unittest.main()
