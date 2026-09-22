import unittest
from gta6_rpc.timer import MonotonicElapsedTimer, format_duration, parse_duration


class TimerTests(unittest.TestCase):
    def test_parse_formats(self):
        self.assertEqual(parse_duration("127:43:29"), 127 * 3600 + 43 * 60 + 29)
        self.assertEqual(parse_duration("12h 34m 56s"), 45296)
        self.assertEqual(parse_duration("90"), 90)

    def test_rejects_invalid_clock_values(self):
        with self.assertRaises(ValueError):
            parse_duration("1:60")
        with self.assertRaises(ValueError):
            parse_duration("1:2:60")

    def test_format(self):
        self.assertEqual(format_duration(0), "0s")
        self.assertEqual(format_duration(45296), "12h 34m 56s")

    def test_monotonic_timer(self):
        values = iter([100.0, 101.2, 102.9, 103.9])
        timer = MonotonicElapsedTimer(10, monotonic=lambda: next(values))
        self.assertEqual(timer.elapsed(), 11)
        self.assertEqual(timer.elapsed(), 12)
        self.assertEqual(timer.elapsed(), 13)


if __name__ == "__main__":
    unittest.main()
