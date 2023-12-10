from checkifvalid import rfc5234
from checkifvalid import rfc5954

# rfc1738
# ; Miscellaneous definitions
DIGITS = r'[' + rfc5234.DIGIT + r']+'
SAFE = r"\$\-\_\.\+"
EXTRA = r"\!\*\'\(\)\,"
UNRESERVED = r'[' + rfc5234.ALPHA + rfc5234.DIGIT + SAFE + EXTRA + r']+'
ESCAPE = r'(?:' + r"%" + rfc5234.HEXDIG + rfc5234.HEXDIG + r')'
UCHAR = r'(?:' + UNRESERVED + r'|' + ESCAPE + r')'

# 5. BNF for specific URL schemes
# URL schemeparts for ip based protocols:
ALPHADIGIT = r'[' + rfc5234.ALPHA + rfc5234.DIGIT + r']'
TOPLABEL = r'(?:' + r'[' + rfc5234.ALPHA + r']' + r'|' + r'(?:' + r'[' + rfc5234.ALPHA + r']' + r'(' + ALPHADIGIT + r'|' + r"-" + r')*' + ALPHADIGIT + r')' + r')'
DOMAINLABEL = r'(?:' + ALPHADIGIT + r'|' + r'(?:' + ALPHADIGIT + r'(?:' + ALPHADIGIT + r'|' + r"-" + r')*' + ALPHADIGIT + r')' + r')'
HOSTNAME = r'(?:' + r'(?:' + DOMAINLABEL + r"\." + r')*' + TOPLABEL + r')'
PORT = DIGITS
HOST = r'(?:' + HOSTNAME + r'|' + rfc5954.IPV4ADDRESS + r'|' + rfc5954.IPV6ADDRESS + r')'
HOSTPORT = r'(?:' + HOST + r'(?:' + r"\:" + PORT + r')?' + r')'
USER = r'(?:' + UCHAR + r'|' + r"\;" + r'|' + r"\?" + r'|' + r"\&" + r'|' + r"\=" + r')*'
PASSWORD = r'(?:' + UCHAR + r'|' + r"\;" + r'|' + r"\?" + r'|' + r"\&" + r'|' + r"\=" + r')*'
LOGIN = r'(?:' + r'(?:' + USER + r'(?:' + ":" + PASSWORD + r')?' + r"\@" + r')?' + HOSTPORT + r')'

# HTTP
SEARCH = r'(?:' + UCHAR + r'|' + r"\;" + r'|' + r"\:" + r'|' + r"\@" + r'|' + r"\&" + r'|' + r"\=" + r')*'
HSEGMENT = r'(?:' + UCHAR + r'|' + r"\;" + r'|' + r"\:" + r'|' + r"\@" + r'|' + r"\&" + r'|' + r"\=" + r')*'
HPATH = r'(?:' + HSEGMENT + r'(?:' + r"\/" + HSEGMENT + r')*' + r')'
HTTPURL = r'(?:' + r"http\:\/\/" + HOSTPORT + r'(?:' + r"\/" + HPATH + r'(?:' + r"\?" + SEARCH + r')?' + r')?' + r')'
HTTPSURL = r'(?:' + r"https\:\/\/" + HOSTPORT + r'(?:' + r"\/" + HPATH + r'(?:' + r"\?" + SEARCH + r')?' + r')?' + r')'


# FTP (see also RFC959)
FTPTYPE = r'(?:' + r"A" + r'|' + r"I" + r'|' + r"D" + r'|' + r"a" + r'|' + r"i" + r'|' + r"d" + r')'
FSEGMENT = r'(?:' + UCHAR + r'|' + r"\?" + r'|' + r"\:" + r'|' + r"\@" + r'|' + r"\&" + r'|' + r"\=" + r')*'
FPATH = r'(?:' + FSEGMENT + r'(?:' + r"\/" + FSEGMENT + r')*' + r')'
FTPURL = r'(?:' + r"ftp\:\/\/" + LOGIN + r'(?:' + r"\/" + FPATH + r'(?:' + r"\;\type\=" + FTPTYPE + r')?' + r')?' + r')'
