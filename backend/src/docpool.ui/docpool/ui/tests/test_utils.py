from docpool.ui.browser.attachments import complete_size_in_bytes

import unittest


class TestUtils(unittest.TestCase):
    """Test helper methods."""

    def test_complete_size_in_bytes(self):
        with self.assertRaises(TypeError):
            self.assertIsNone(complete_size_in_bytes(None))

        with self.assertRaises(ValueError):
            self.assertEqual(complete_size_in_bytes(["Foo"]), None)

        with self.assertRaises(ValueError):
            self.assertEqual(complete_size_in_bytes("Foo"), None)

        self.assertEqual(complete_size_in_bytes(["12 MB", "335,5 kb", "12 b"]), 12926476.0)
        self.assertEqual(complete_size_in_bytes(["1 MB", "0 Mb", "12 b"]), 1048588.0)
        self.assertEqual(complete_size_in_bytes(["12 MB", None, "12 b"]), 12582924.0)
        self.assertEqual(complete_size_in_bytes(["12 MB", 0, "12 b"]), 12582924.0)
        self.assertEqual(complete_size_in_bytes(["1 GB"]), 1073741824.0)
