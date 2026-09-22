import unittest
from gta6_rpc.config import build_config
from gta6_rpc.validation import validate_config


def valid_data():
    return {
        "client_id": "123456789",
        "played_time": {"hours": 1, "minutes": 2, "seconds": 3},
        "update_interval": 1,
        "activity_rotation": {"enabled": True, "min_seconds": 60, "max_seconds": 120},
        "assets": {"large_image": "gta6_brl", "large_text": "GTA VI"},
        "buttons": [{"label": "Rockstar", "url": "https://www.rockstargames.com/VI"}],
        "activities": ["Exploring Vice City"],
        "locations": ["Vice City"],
        "details_suffixes": ["Free Roam"],
    }


class ValidationTests(unittest.TestCase):
    def test_valid_config(self):
        self.assertEqual(validate_config(build_config(valid_data())), [])

    def test_rotation_order(self):
        data = valid_data()
        data["activity_rotation"]["min_seconds"] = 200
        data["activity_rotation"]["max_seconds"] = 100
        errors = validate_config(build_config(data))
        self.assertTrue(any("rotation_min_seconds" in e for e in errors))

    def test_bad_url(self):
        data = valid_data()
        data["buttons"][0]["url"] = "not-a-url"
        errors = validate_config(build_config(data))
        self.assertTrue(any("url" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
