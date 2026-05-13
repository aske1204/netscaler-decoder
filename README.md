# NetScaler Cookie Decoder

Decodes Citrix NetScaler persistence cookies to reveal the backend server IP address and port they encode.

## Background

NetScaler load balancers insert a cookie (typically named `NSC_*`) into HTTP responses to maintain session persistence. The cookie value encodes the destination server's IP and port as XOR-obfuscated hex, using fixed keys:

| Field | XOR key    |
|-------|------------|
| IP    | `0x03081E11` |
| Port  | `0x3630`     |

The cookie format is a hex string where:
- bytes 9–16 (the second group of 8 hex chars) encode the IP
- the final 4 hex chars encode the port

## Usage

### As a script

```bash
python3 decode.py <cookie_value> [cookie_value ...]
```

```
$ python3 decode.py 000000002c20f97900002000
Cookie : 000000002c20f97900002000
  IP   : 47.40.231.104
  Port : 4160
```


## Requirements

Python 3.6+ — no third-party dependencies.

## Example: finding the cookie in a real response

NetScaler cookies are usually named with an `NSC_` prefix. You can extract the value with:

```bash
curl -sI https://target.example.com | grep -i 'set-cookie: NSC_'
```

Then pass the hex value (the part after `=`, before any `;`) to the decoder.

