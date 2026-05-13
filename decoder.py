import re
import sys


def decode_netscaler_cookie(cookie_val: str) -> str:
    m = re.search(r'[0-9a-f]{8}([0-9a-f]{8}).*([0-9a-f]{4})$', cookie_val)
    if not m:
        raise ValueError(f"Cookie value did not match expected format: {cookie_val!r}")

    ip_value   = int(m.group(1), 16) ^ 0x03081E11
    port_value = int(m.group(2), 16) ^ 0x3630

    ip_hex = f"{ip_value:08X}"
    ip = ".".join(str(int(ip_hex[i:i+2], 16)) for i in range(0, 8, 2))

    return ip, port_value


if __name__ == "__main__":
    cookies = sys.argv[1:]
    for cookie in cookies:
        ip, port = decode_netscaler_cookie(cookie)
        print(f"Cookie : {cookie}")
        print(f"  IP   : {ip}")
        print(f"  Port : {port}")
        print()
