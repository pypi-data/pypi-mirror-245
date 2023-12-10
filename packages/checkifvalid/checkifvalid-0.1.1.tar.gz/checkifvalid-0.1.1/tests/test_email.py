import unittest
import checkifvalid

valid_text = [
    "john.doe@example.com",
    "abc-@mail.com",
    "abc@mail.com",
    "abc_def@mail.com",
    "abc.def@mail-archive.com",
    "abc+def@mail.com",
]

invalid_text = [
    "@mail.com",
    "mail.com",
    ".abc@mail.com",
    "abc..def@mail.com",
    "john@doe@mail.com",
]

class TestEmail(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.email(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.email(b))