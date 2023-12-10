import unittest
import checkifvalid

valid_text = [
    "https://john.doe@www.example.com:123/forum/questions/?tag=networking&der=newest#top",
    "http://192.168.1.1:80",
    "https://www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg",
    "https://www.google.com",
    "ftp://ftp.uk.linux.org/pub/linux/Networking/netkit",
    "http://www.ietf.org/rfc/rfc2396.txt",
    "https://mail.google.com/mail/u/0/#inbox",
    "https://news.google.com/home?hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/articles/CAIiENDJrE9KPQLhdpgRHrpcH4jekEifjHCx8jCoUCAoiEImmCk2lY-I3pBIn4xwsfIww37rKBg?hl=en-US&gl=US&ceid=US%3Aen"
]

invalid_text = [
    "htts://www.google.com",
    "http:/\www.google.com",
    "http://-abcdef.168.1.1",
    "-https:/abcdef/www.google.fr/",
    "https:/abcdef/www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg",
]

class TestUrl(unittest.TestCase):
    def test_valid(self):
        """checking valid syntax"""
        for v in valid_text:
            self.assertTrue(checkifvalid.url(v))
            
    def test_invalid(self):
        """checking invalid syntax"""
        for b in invalid_text:
            self.assertFalse(checkifvalid.url(b))


