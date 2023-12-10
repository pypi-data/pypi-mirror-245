import unittest
import checkifvalid

valid_text = [
    "::",
    "::1",
    "FFFF:AAAA::221:3:11:3",
    "::FFFF:10.2.4.1",
    "2001:0:42:3:ff::1",
    "2003:dead:beef:4dad:ab33:46:abab:62",
]

invalid_text = [
    "FFFF:AAAA:;:221:3:11:3",
    "fe80:2030:31:24",
    "255.1.4.2",
]

class TestIp6(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.ipv6_address(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.ipv6_address(b))