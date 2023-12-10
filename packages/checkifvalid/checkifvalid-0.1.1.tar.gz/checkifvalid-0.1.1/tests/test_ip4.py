import unittest
import checkifvalid

valid_text = [
    "127.0.0.1",
    "255.255.255.255",
    "0.0.0.0",
]

invalid_text = [
    "127.0.-.1",
    "a.b.c.f",
    "127.0.1",
    "257.0.0.1",
    "192.168.1.9999",
    "192.168.000.254"
]

class TestIp4(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.ipv4_address(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.ipv4_address(b))