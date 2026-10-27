import unittest
from datetime import datetime
from alarm import next_alarm


class ScheduleTests(unittest.TestCase):
    def test_today(self):
        self.assertEqual(next_alarm('07:30', datetime(2026, 10, 27, 6)), datetime(2026, 10, 27, 7, 30))

    def test_next_day_after_time_passed(self):
        self.assertEqual(next_alarm('07:30', datetime(2026, 10, 27, 8)), datetime(2026, 10, 28, 7, 30))

    def test_year_boundary(self):
        self.assertEqual(next_alarm('00:01', datetime(2026, 12, 31, 23, 59)), datetime(2027, 1, 1, 0, 1))

    def test_invalid(self):
        for value in ('24:00', '12:60', 'abc', '', '07:30:00', '-1:20'):
            with self.assertRaises(ValueError):
                next_alarm(value, datetime.now())


if __name__ == '__main__':
    unittest.main()
