import unittest
import checkifvalid

valid_text = [
    "FF:FF:FF:FF:FF:FF",
    "00:11:22:33:44:55",
]

invalid_text = [
    "FF:FF:FF",
    "FF:FF:FF:FF:FF:GG",
]

class TestMacAddr(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.mac_address(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.mac_address(b))