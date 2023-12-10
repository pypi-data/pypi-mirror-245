import unittest
import checkifvalid

valid_text = [
    "sip:support@john.doe",
    "sip:support@john.doe:443",
    "ssh://userid@address.com",
    "ssh://userid:password@address.com/?x11=display-location&exec=exec-bin-path",
    "ssh://192.168.1.100",
    "ssh://192.168.1.100:22",
    "foo://example.com:8042/over/there?name=ferret#nose",
    "telnet://192.0.2.16:80/",
    "mailto://john@doe.fr"
]

invalid_text = [
    ".abcdef://abcdef.168.1.1",
    "telnet://168.1.1.1:aaaa",
]

class TestUri(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.uri(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.uri(b))


