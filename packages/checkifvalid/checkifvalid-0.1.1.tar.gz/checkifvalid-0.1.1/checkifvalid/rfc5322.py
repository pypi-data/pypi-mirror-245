
from checkifvalid import rfc5234

# Internet Message Format rfc5322

# 3.2.1.  Quoted characters
QUOTED_PAIR = r'(?:' + r'(?:' + r"\\" + r'(?:' + rfc5234.VCHAR + r'|' + rfc5234.WSP + r')' + r')' + r'|' + r')'

# 3.2.2.  Folding White Space and Comments
FWS = r'(?:' + r'(?:' + r'(?:' + rfc5234.WSP + r'*' + rfc5234.CRLF + r')?' + rfc5234.WSP + r'+' + r')' + r')'   # Folding white space

# Non white space controls  ; The rest of the US-ASCII ;  characters not
# including "(", ;  ")", or "\"
CTEXT = r'(?:' + r'|' + r'\x21-\x27' + r'|' + r'\x2A-\x5B' + r'|' + r'\x5D-\x7E' + r'|' + r')'
CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'
COMMENT = r'(?:' + r'\(' + r'(?:' + FWS + r'?' + CCONTENT + r')*' + FWS + r'?' + r'\)' + r')'
CFWS = r'(?:' + r'(?:' + r'(?:' + FWS + r'?' + COMMENT + r')+' + FWS + r'?' + r')' + r'|' + FWS + r')'

# 3.2.3.  Atom
# Any character except controls,;  SP, and specials.  ;  Used for atoms
ATEXT = r'[' + rfc5234.ALPHA + rfc5234.DIGIT + r"\!\#\$\%\&\'\*\+\-\/=\?\^\_\`\{\|\}\~]"
ATOM = r'(?:' + CFWS + r'?' + ATEXT + r'+' + CFWS + r'?' + r')'
DOT_ATOM_TEXT = r'(?:' + ATEXT + r'+' + r'(?:' + r"\." + ATEXT + r'+' + r')*' + r')'
DOT_ATOM = r'(?:' + CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' + r')'

# 3.2.4.  Quoted Strings
QTEXT = r'[' + r'\x21' + r'\x23-\x5B' + r'\x5D-\x7E' + r']'
QCONTENT = r'(?:' + QTEXT + r'|' + QUOTED_PAIR + r')'
QUOTED_STRING = r'(?:' + CFWS + r'?' + rfc5234.DQUOTE + r'(' + FWS + r'?' + QCONTENT + r')*' + FWS + r'?' + rfc5234.DQUOTE + CFWS + r'?' + r')'

# 3.2.5.  Miscellaneous Tokens
WORD = r'(?:' + ATOM + r'|' + QUOTED_STRING + r')'

# 3.4.1.  Addr-Spec Specification
DTEXT = r'[' + r'\x21-\x5A\x5E-\x7E' + r']'
DOMAIN_LITERAL = r'(?:' + CFWS + r'?' + r"\[" + r'(?:' + FWS + r'?' + r'(?:' + DTEXT + r'|' + r')' + r')*' + FWS + r'?' + r"\]" + CFWS + r'?' + r')'
DOMAIN = r'(?:' + DOT_ATOM + r'|' + DOMAIN_LITERAL + r')' #  + r'|' + OBS_DOMAIN 
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + QUOTED_STRING + r')' # + r'|' + OBS_LOCAL_PART 
ADDR_SPEC = r'(?:' + LOCAL_PART + r"@" + DOMAIN + r')'