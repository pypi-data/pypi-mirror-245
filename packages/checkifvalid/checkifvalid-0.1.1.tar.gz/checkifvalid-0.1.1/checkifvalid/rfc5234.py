
# Augmented BNF for Syntax Specifications: ABNF

# B.1.  Core Rules . . . . . . . . . . . . . . . . . . . . . . . . 13

# controls
CTL = r'[\x00-\x1F\x7F]'                      

# carriage return
CR = r'\x0D'                                 

# 0-9
DIGIT = r'\x30-\x39'                                

# " (Double Quote)
DQUOTE = r'\x22'                                 

# visible (printing) characters
VCHAR = r'[\x21-\x7E]'                          

# 8 bits of data
OCTET = r'[\x00-\xFF]'                          

# linefeed
LF = r'\x0A'                                 

# horizontal tab
HTAB = r'\x09'                                 
SP = r'\x20'

# white space
WSP = r'(?:' + SP + r'|' + HTAB + r')'                    

#  Internet standard newline
CRLF = r'(?:' + CR + LF + r')'
HEXDIG = r'[' + DIGIT + r'ABCDEFabcdef]'

# any 7-bit US-ASCII character, excluding NUL
CHAR = r'[\x01-\x7F]'
BIT = r'[01]'

# A-Z / a-z
ALPHA = r'\x41-\x5A\x61-\x7A'      

# linear white space
LWSP = r'(?:' + WSP + r'|' + r'(' + CRLF + WSP + r')' + r')*'
