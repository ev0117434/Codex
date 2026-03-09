import unittest

from snapshot.healthcheck import get_status


class TestHealthcheck(unittest.TestCase):
    def test_status(self):
        status = get_status("config/config.yaml")
        self.assertEqual(status["status"], "ok")
        self.assertEqual(status["service"], "spread-monitor")


if __name__ == "__main__":
    unittest.main()
