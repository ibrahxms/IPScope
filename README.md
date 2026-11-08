# IPScope

<img width="978" height="513" alt="image" src="https://github.com/user-attachments/assets/3ddd6c11-9d70-41b2-9610-055b9e92d51b" />


A fast, colorful terminal tool for looking up IP addresses: location, ISP, ASN, and VPN / proxy detection, with a one-key jump to the map.

**Made by [ibrahxms](https://github.com/ibrahxms)** | [guns.lol/ibrahxm](https://guns.lol/ibrahxm)

## Features

- Country, region, city, ZIP, timezone, and coordinates
- ISP, organization, and ASN
- VPN / proxy / Tor detection from two sources, plus datacenter, mobile, and abuse flags
- Clickable OpenStreetMap link with a pin, and an option to open it in your browser
- Leave the IP blank to look up your own
- Keeps running if a lookup fails and shows the error instead of closing

## Install

Requires Python 3.8+.

```bash
git clone https://github.com/ibrahxms/ipscope.git
cd ipscope
pip install -r requirements.txt
```

## Usage

```bash
python ipscope.py
```

1. Pick **1** for IP lookup
2. Enter an IP address, or press Enter to look up your own
3. Type `y` at the prompt to open the location in your browser

## Data sources

| Source | Used for |
| --- | --- |
| [ip-api.com](https://ip-api.com) | Location, ISP, ASN, proxy flag |
| [ipapi.is](https://ipapi.is) | Second opinion on VPN / proxy / Tor |

Both are free and need no API key. ip-api.com's free tier is HTTP only and limited to about 45 requests per minute. ipapi.is allows about 1,000 requests per day. If ipapi.is can't be reached, IPScope still works using ip-api.com alone.

## Notes

- IP geolocation is approximate, usually accurate to the city or neighborhood, not a street address.
- VPN and proxy detection is not perfect. Residential VPNs and private proxies can go undetected, so "not detected" does not guarantee a clean connection.
- Only look up IP addresses you have a legitimate reason to check.

## License

MIT, see [LICENSE](LICENSE).
