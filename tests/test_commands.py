"""Tests for Maya's initial command handler."""

import unittest

from maya.commands import handle_command


class MayaCommandTests(unittest.TestCase):
    def test_hello(self):
        response, running = handle_command("hello")
        self.assertIn("Maya", response)
        self.assertTrue(running)

    def test_help(self):
        response, running = handle_command("help")
        self.assertIn("search", response.lower())
        self.assertTrue(running)

    def test_exit(self):
        response, running = handle_command("exit")
        self.assertFalse(running)
        self.assertIn("Goodbye", response)

    def test_unknown_command(self):
        response, running = handle_command("make me a website")
        self.assertIn("don't know", response.lower())
        self.assertTrue(running)

    def test_search(self):
        response, running = handle_command("search Python tutorials")
        self.assertIn("google.com/search", response)
        self.assertTrue(running)

    def test_empty_command(self):
        response, running = handle_command("   ")
        self.assertEqual(response, "")
        self.assertTrue(running)


if __name__ == "__main__":
    unittest.main()
