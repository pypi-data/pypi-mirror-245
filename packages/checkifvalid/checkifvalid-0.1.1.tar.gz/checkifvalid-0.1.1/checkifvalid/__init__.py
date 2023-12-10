from checkifvalid import rfc5954
from checkifvalid import rfc5322
from checkifvalid import rfc3986
from checkifvalid import rfc1738

import re

PATTERN_IPV4 = re.compile(r'^%s$' % rfc5954.IPV4ADDRESS)
PATTERN_IPV6 = re.compile(r'^%s$' % rfc5954.IPV6ADDRESS)
PATTERN_MAC = re.compile(r'^%s$' % rfc5954.MACADDRESS)

PATTERN_HOSTNAME = re.compile(r'^%s$' % rfc1738.HOSTNAME)
PATTERN_EMAIL = re.compile(r'^%s$' % rfc5322.ADDR_SPEC)

PATTERN_URI = re.compile(r'^%s$' % rfc3986.URI)
PATTERN_URL = re.compile(r'^%s|%s|%s$' % (rfc1738.HTTPURL,rfc1738.HTTPSURL,rfc1738.FTPURL))

def email(text):
    """Email syntax is valid?"""
    if PATTERN_EMAIL.match(text) is None:
        return False

    # total length of 320 characters
    if len(text) > 320:
        return False

    local_part, domain_part = text.split('@', 1)

    #  That limit is a maximum of 64 characters (octets) in the "local part"
    if len(local_part) > 64:
        return False

    # a maximum of 255 characters (octets) in the domain part
    if len(domain_part) > 255:
        return False
    
    return True

def hostname(text):
    """Hostname syntax is valid?"""
    if PATTERN_HOSTNAME.match(text) is None:
        return False

    # A complete, fully-qualified, domain name must not exceed 255 octets.
    if len(text) > 255:
        return False

    return True

def ipv6_address(text):
    """IPv6 address is valid ?"""
    if PATTERN_IPV6.match(text) is None:
        return False
    return True

def ipv4_address(text):
    """IPv4 address is valid ?"""
    if PATTERN_IPV4.match(text) is None:
        return False
    return True

def mac_address(text):
    """MAC address is valid ?"""
    if PATTERN_MAC.match(text) is None:
        return False
    return True

def url(text):
    """HTTP url is valid?"""
    if PATTERN_URL.match(text) is None:
        return False
    return True

def uri(text):
    """URI is valid ?"""
    if PATTERN_URI.match(text) is None:
        return False
    return True