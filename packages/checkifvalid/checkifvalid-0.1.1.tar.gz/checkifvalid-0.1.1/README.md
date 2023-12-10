# What is this?

Syntax validator compliant to RFC specifications for
- Email
- Hostname
- URL
- URI
- IPv4 and IPv6
- Mac address 

## Installation

This module can be installed from [pypi](https://pypi.org/project/checkifvalid/) website

```bash
pip install checkifvalid
```

## Checking IPv4 or IPv6 syntax

```python
import checkifvalid

checkifvalid.ipv6_address("::1")
True

checkifvalid.ipv4_address("127.0.0.1")
True

checkifvalid.ipv4_address("127.0.0.257")
False
```

## Checking URL syntax

```python
import checkifvalid

checkifvalid.url("https://www.google.com")
True
```

## Other syntax validator

```python
import checkifvalid

checkifvalid.email("john.doe@example.com")
True

checkifvalid.uri("sip:support@john.doe:443",)
True

checkifvalid.mac_address("00:11:22:33:44:55")
True

checkifvalid.hostname("john@doe")
False
```

## For developpers

Run test units

```bash
python3 -m unittest discover tests/ -v
```