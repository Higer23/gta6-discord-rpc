import sys
import types
import unittest

from gta6_rpc.rpc_client import DiscordRPCClient


class FakePresence:
    instances = []

    def __init__(self, client_id):
        self.client_id = client_id
        self.updates = []
        self.closed = False
        self.fail_pipe = False
        FakePresence.instances.append(self)

    def connect(self):
        return None

    def update(self, **payload):
        if self.fail_pipe:
            raise FakePipeClosed("closed")
        self.updates.append(payload)

    def clear(self):
        return None

    def close(self):
        self.closed = True


class FakePipeClosed(Exception):
    pass


class RPCClientTests(unittest.TestCase):
    def setUp(self):
        self.old = sys.modules.get("pypresence")
        module = types.ModuleType("pypresence")
        module.Presence = FakePresence
        module.exceptions = types.SimpleNamespace(PipeClosed=FakePipeClosed)
        sys.modules["pypresence"] = module
        FakePresence.instances.clear()

    def tearDown(self):
        if self.old is None:
            sys.modules.pop("pypresence", None)
        else:
            sys.modules["pypresence"] = self.old

    def test_mock_update(self):
        client = DiscordRPCClient("123", quiet=True)
        self.assertTrue(client.connect(wait=False))
        self.assertTrue(client.update({"details": "test"}))
        self.assertEqual(FakePresence.instances[-1].updates[0]["details"], "test")
        client.close()

    def test_pipe_reconnect(self):
        client = DiscordRPCClient("123", quiet=True)
        client.connect(wait=False)
        FakePresence.instances[-1].fail_pipe = True
        self.assertFalse(client.update({"details": "test"}))
        self.assertTrue(client.connected)
        self.assertGreaterEqual(len(FakePresence.instances), 2)
        client.close()


if __name__ == "__main__":
    unittest.main()
