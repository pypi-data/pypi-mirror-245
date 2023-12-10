from checkifvalid import rfc5234
from checkifvalid import rfc5954

# Appendix A. Collected ABNF for URI
PCT_ENCODED = r'(?:' + r"\%" + rfc5234.HEXDIG + rfc5234.HEXDIG + r')'
UNRESERVED_RFC3986 = r'[' + rfc5234.ALPHA + rfc5234.DIGIT + r"\-\.\_\~" + r']+'
GEN_DELIMS = r'(?:' + r"\:" + r'|' + r"\/" + r'|' + r"\?" + r'|' + r"\#" + r'|' + r"\[" + r'|' + r"\]" + r'|' + r"\@" + r')'
SUB_DELIMS = r'(?:' + r"\!" + r'|' + r"\$" + r'|' + r"\&" + r'|' + r"\'" + r'|' + r"\(" + r'|' + r"\)" + r'|' + r"\*" + r'|' + r"\+" + r'|' + r"\," + r'|' + r"\;" + r'|' + r"\=" + r')'
RESERVED = r'(?:' + GEN_DELIMS + r'|' + SUB_DELIMS + r')'
PCHAR = r'(?:' + UNRESERVED_RFC3986 + r'|' + PCT_ENCODED + r'|' + SUB_DELIMS + r'|' + r"\:" + r'|' + r"\@" + r')'
QUERY = r'(?:' + PCHAR + r'|' + r"\/" + r'|' + r"\?" + r')*'
FRAGMENT = r'(?:' + PCHAR + r'|' + r"\/" + r'|' + r"\?" + r')*'

SEGMENT = r'(?:' + PCHAR + r')*'
SEGMENT_NZ = r'(?:' + PCHAR + r')+'

# non-zero-length segment without any colon ":"
SEGMENT_NZ_NC = r'(?:' + UNRESERVED_RFC3986 + r'|' + PCT_ENCODED + r'|' + SUB_DELIMS + r'|' + r"\@" + r')+'  

PATH_EMPTY = r'(?:' + PCHAR + r'){0}'
PATH_ROOTLESS = r'(?:' + SEGMENT_NZ + r'(?:' + r"/" + SEGMENT + r')*' + r')'
PATH_ABSOLUTE = r'(?:' + r"/" + r'(?:' + SEGMENT_NZ + r'(?:' + r"/" + SEGMENT + r')*' + r')?' + r')'
PATH_ABEMPTY = r'(?:' + r"/" + SEGMENT + r')*'

USERINFO = r'(?:' + UNRESERVED_RFC3986 + r'|' + PCT_ENCODED + r'|' + SUB_DELIMS + r'|' + r"\:" + r')*'
REG_NAME = r'(?:' + UNRESERVED_RFC3986 + r'|' + PCT_ENCODED + r'|' + SUB_DELIMS + r')*'
IPVFUTURE = r'(?:' + r"v" + rfc5234.HEXDIG + r"+" + r"\." + r'(?:' + UNRESERVED_RFC3986 + r'|' + SUB_DELIMS + r'|' + r"\:" + r')*' + r')'
IP_LITERAL = r'(?:' + r"\[" + r'(?:' + rfc5954.IPV6ADDRESS + r'|' + IPVFUTURE + r')' + r"\]" + r')'
HOST_RFC3986 = r'(?:' + IP_LITERAL + r'|' + rfc5954.IPV4ADDRESS + r'|' + REG_NAME + r')'
PORT_RFC3986 = r'(?:[' + rfc5234.DIGIT + r'])*'
AUTHORITY = r'(?:' + r'(?:' + USERINFO + r"\@" + r')?' + HOST_RFC3986 + r'(?:' + r"\:" + PORT_RFC3986 + r')?' + r')'

HIER_PART = r'(?:' + r'(?:' + r"//" + AUTHORITY + PATH_ABEMPTY + r')' + r'|' + PATH_ABSOLUTE + r'|' + PATH_ROOTLESS + r'|' + PATH_EMPTY + r')'
SCHEME = r'(?:' + r'[' + rfc5234.ALPHA + r']' + r'(?:' + r'[' + rfc5234.ALPHA + r']' + r'|' + r'[' + rfc5234.DIGIT + r']' + r'|' + r"\+" + r'|' + r"\-" + r'|' + r"\." + r')*' + r')'
URI = r'(?:' + SCHEME + r":" + HIER_PART + r'(?:' + r"\?" + QUERY + r')?' + r'(?:' + r"\#" + FRAGMENT + r')?' + r')'