import unittest
from unittest.mock import patch, MagicMock
from main import PyServer
from client import PyClient
import socket
import platform


class TestPyServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Determine the operating system once before running the tests."""
        cls.os = platform.system()

    def setUp(self):
        """Create a new PyServer instance before each test."""
        self.server = PyServer()

    def test_methodPrep(self):
        """Test that methodPrep processes users, PIDs and ports."""
        methods = ["users", "pids", "ports"]
        conn = MagicMock()
        addr = ("127.0.0.1", 12345)

        self.server.enumeration = MagicMock()
        self.server.methodPrep(methods, conn, addr)

        self.assertEqual(self.server.enumeration.call_count, 3)

        calls = self.server.enumeration.call_args_list

        self.assertEqual(calls[0].args[0], "users")
        self.assertEqual(calls[1].args[0], "pids")
        self.assertEqual(calls[2].args[0], "ports")

    @patch("client.socket.socket")
    def test_connection(self, mock_socket):
        """Test that the client creates a TCP socket and connects to the server."""
        client = PyClient()
        client.commands = MagicMock()

        client.connection()

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket().connect.assert_called_once_with(("127.0.0.1", 12345))
        client.commands.assert_called_once()

    def test_client_functions(self):
        """Test the client enumeration functions for the current operating system."""
        client = PyClient()

        if self.os == "Linux":
            client.linUsers()
            self.assertNotEqual(client.users, "\n")
            self.assertIn("| ", client.users)

            pids = client.linPids()
            self.assertIsInstance(pids, str)
            self.assertNotEqual(pids, "")

            suids = client.linSUID()
            self.assertIsInstance(suids, str)

        elif self.os == "Windows":
            users = client.winUsers()
            self.assertIsInstance(users, str)

            pids = client.linPids()
            self.assertIsInstance(pids, str)
            self.assertNotEqual(pids, "")

            ports = client.winScanner()
            self.assertIsInstance(ports, str)


if __name__ == "__main__":
    unittest.main(verbosity=2)
