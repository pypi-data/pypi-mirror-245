
from checkifvalid import rfc5234

# rfc5954 Essential Correction for IPv6 ABNF and URI Comparison in RFC 3261
# 4.1. Resolution for Extra Colon in IPv4-Mapped IPv6 Address
D0 = r'[' + rfc5234.DIGIT + r']'
D10 = r'(?:' + r'[' + r'\x31-\x39' + r']' + D0 + r')'
D100 = r'(?:' + r"1" + D0 + r'{2}' + r')'
D200 = r'(?:' + r"2" + r'[' + r'\x30-\x34' + r']' + D0 + r')'
D250 = r'(?:' + r"25" + r'[' + r'\x30-\x35' + r']' + r')'
D8 = r'(?:' + D0 + r'|' + D10 + r'|' + D100 + r'|' + D200 + r'|' + D250 + r')'
IPV4ADDRESS = r'(?:' + D8 + r"\." + D8 + r"\." + D8 + r"\." + D8 + r')'


H16 = r'(?:' + rfc5234.HEXDIG + r'{1,4}' + r')'
LS32 = r'(?:' + r'(?:' + H16 + r"\:" + H16 + r')' + r'|' + IPV4ADDRESS + r')'

IPV6_FORM1 = r'(?:' + r'(?:' + H16 + r":" + r'){6}' + LS32 + r')'
IPV6_FORM2 = r'(?:' + r"::" + r'(?:' + H16 + r":" + r'){5}' + LS32 + r')'
IPV6_FORM3 = r'(?:' + H16 + r'?' + r"::" + r'(?:' + H16 + r":" + r'){4}' + LS32 + r')'
IPV6_FORM4 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r')?' + H16 + r')' + r'?' + r"::" + r'(?:' + H16 + r":" + r'){3}' + LS32 + r')'
IPV6_FORM5 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r'){0,2}' + H16 + r')' + r'?' + r"::" + r'(?:' + H16 + r":" + r'){2}' + LS32 + r')'
IPV6_FORM6 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r'){0,3}' + H16 + r')' + r'?' + r"::" + r'(?:' + H16 + r":" + r')' + LS32 + r')'
IPV6_FORM7 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r'){0,4}' + H16 + r')' + r'?' + r"::" + LS32 + r')'
IPV6_FORM8 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r'){0,5}' + H16 + r')' + r'?' + r"::" + H16 + r')'
IPV6_FORM9 = r'(?:' + r'(?:' + r'(?:' + H16 + r":" + r'){0,6}' + H16 + r')' + r'?' + r"::" + r')'

IPV6ADDRESS = r'(?:' + IPV6_FORM1 + r'|' + IPV6_FORM2 + r'|' + IPV6_FORM3 + r'|' + IPV6_FORM4 + r'|' + IPV6_FORM5 + r'|' + IPV6_FORM6 + r'|' + IPV6_FORM7 + r'|' + IPV6_FORM8 + r'|' + IPV6_FORM9 + r')'

OCTET = r'(?:' + rfc5234.HEXDIG + r'{2}' + r')'
MACADDRESS = r'(?:' + OCTET + r':' + OCTET + r':' + OCTET + r':' + OCTET + r':' + OCTET + r':' + OCTET + r')'
