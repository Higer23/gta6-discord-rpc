import unittest
from gta6_rpc.config import build_config
from gta6_rpc.models import PresenceState
from gta6_rpc.presence import PresenceBuilder


class PresenceTests(unittest.TestCase):
    def test_payload_sanitizes_buttons(self):
        data = {
            "client_id": "123",
            "played_time": {"hours": 1},
            "assets": {"large_image": "gta6_brl"},
            "buttons": [
                {"label": "Good", "url": "https://example.com"},
                {"label": "Second", "url": "https://example.com"},
                {"label": "Third", "url": "https://example.com"},
            ],
            "activities": ["Explore"],
            "locations": ["Vice City"],
            "details_suffixes": ["Free Roam"],
        }
        config = build_config(data)
        state = PresenceState(3600, 100, "Explore", "Vice City", "Free Roam")
        payload = PresenceBuilder(config).build(state)
        self.assertEqual(len(payload["buttons"]), 2)
        self.assertEqual(payload["start"], 100)


if __name__ == "__main__":
    unittest.main()
