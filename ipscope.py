#!/usr/bin/env python3
"""
IPScope - terminal IP lookup tool
made by ibrahxms
  guns.lol/ibrahxm
  https://github.com/ibrahxms

Usage:  pip install requests  &&  python ipscope.py
Data:   ip-api.com (location) + ipapi.is (VPN/proxy check)
"""

import json
import os
import sys
import webbrowser

try:
    import requests
except ImportError:
    print("missing dependency -> run: pip install requests")
    input("press enter to close...")
    sys.exit(1)

# ---------- config ----------
TIMEOUT = 8
VERSION = "1.0"

# ---------- colors ----------
if os.name == "nt":
    os.system("")  # enables ANSI colors on Windows terminals

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
M = "\033[95m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = f"""{M}{BOLD}
  ___ ____  ____                       
 |_ _|  _ \\/ ___|  ___ ___  _ __   ___ 
  | || |_) \\___ \\ / __/ _ \\| '_ \\ / _ \\
  | ||  __/ ___) | (_| (_) | |_) |  __/
 |___|_|   |____/ \\___\\___/| .__/ \\___|
                           |_|        {RESET}
 {DIM}v{VERSION}  |  made by {RESET}{BOLD}ibrahxms{RESET}
 {C}guns.lol/ibrahxm{RESET}  {DIM}|{RESET}  {C}github.com/ibrahxms{RESET}
"""


# ---------- helpers ----------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def prompt(text):
    try:
        return input(f"{M}[?]{RESET} {text}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def err(text):
    print(f"{R}[!]{RESET} {text}")


def kv(key, value, color=RESET):
    value = "-" if value is None or value == "" else value
    print(f"  {C}{key:<12}{RESET} {DIM}>{RESET} {color}{value}{RESET}")


def pause():
    try:
        input(f"\n{DIM}press enter to continue...{RESET}")
    except (EOFError, KeyboardInterrupt):
        print()


# ---------- modules ----------
IPAPI_FIELDS = (
    "status,message,country,countryCode,regionName,city,zip,lat,lon,"
    "timezone,isp,org,as,mobile,proxy,hosting,query"
)
SECURITY_URL = "https://api.ipapi.is/"  # second opinion for VPN / proxy / Tor


def security_check(ip):
    """Best-effort VPN/proxy/Tor lookup. Returns a dict, or {} if unavailable."""
    try:
        d = requests.get(SECURITY_URL, params={"q": ip}, timeout=TIMEOUT).json()
        return d if isinstance(d, dict) and "error" not in d else {}
    except (requests.RequestException, ValueError):
        return {}


def module_ip():
    target = prompt("enter IP (blank = your own IP)")
    url = f"http://ip-api.com/json/{target}?fields={IPAPI_FIELDS}"
    try:
        data = requests.get(url, timeout=TIMEOUT).json()
    except (requests.RequestException, ValueError) as e:
        err(f"request failed: {e}")
        pause()
        return

    if data.get("status") != "success":
        err(f"lookup failed: {data.get('message', 'unknown error')}")
        pause()
        return

    ip = data.get("query", "-")
    sec = security_check(ip)

    print()
    kv("IP ADDRESS", ip)
    kv("COUNTRY", f"{data.get('country', '-')} ({data.get('countryCode', '-')})")
    kv("REGION", data.get("regionName", "-"))
    kv("CITY", data.get("city", "-"))
    kv("ZIP", data.get("zip", "-"))
    kv("TIMEZONE", data.get("timezone", "-"))
    kv("ISP", data.get("isp", "-"))
    kv("ORG", data.get("org", "-"))
    kv("ASN", data.get("as", "-"))
    kv("COORDINATES", f"{data.get('lat', '-')}, {data.get('lon', '-')}")

    # ---- VPN / proxy detection (ip-api flag + ipapi.is second opinion) ----
    vpn = bool(sec.get("is_vpn"))
    tor = bool(sec.get("is_tor"))
    proxy = bool(data.get("proxy")) or bool(sec.get("is_proxy"))
    hosting = bool(data.get("hosting")) or bool(sec.get("is_datacenter"))

    if vpn or tor or proxy:
        kinds = [n for n, on in (("VPN", vpn), ("PROXY", proxy), ("TOR", tor)) if on]
        kv("VPN/PROXY", f"{R}DETECTED ({' + '.join(kinds)}){RESET}")
    else:
        kv("VPN/PROXY", f"{G}NOT DETECTED{RESET}")

    flags = []
    if hosting:
        flags.append(f"{Y}DATACENTER/HOSTING{RESET}")
    if data.get("mobile") or sec.get("is_mobile"):
        flags.append(f"{C}MOBILE NETWORK{RESET}")
    if sec.get("is_abuser"):
        flags.append(f"{Y}ABUSE FLAGGED{RESET}")
    if flags:
        kv("FLAGS", " ".join(flags))
    if not sec:
        kv("NOTE", f"{DIM}second VPN check unavailable, using ip-api only{RESET}")

    lat, lon = data.get("lat"), data.get("lon")
    if lat is not None and lon is not None:
        map_url = (
            f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}"
            f"#map=13/{lat}/{lon}"
        )
        # OSC 8 makes the link clickable in most modern terminals (Ctrl+click)
        link = f"\033]8;;{map_url}\033\\{map_url}\033]8;;\033\\"
        kv("MAP", link, C)
        if prompt("open map in browser? (y/N)").lower() in ("y", "yes"):
            try:
                if not webbrowser.open(map_url):
                    err("couldn't launch a browser, copy the link above instead")
            except Exception as e:
                err(f"couldn't open browser: {e}")
    pause()


def module_about():
    print()
    kv("TOOL", f"IPScope v{VERSION}")
    kv("MADE BY", "ibrahxms", BOLD)
    kv("BIO", "guns.lol/ibrahxm", C)
    kv("GITHUB", "https://github.com/ibrahxms", C)
    kv("DATA", "ip-api.com + ipapi.is")
    pause()


# ---------- main loop ----------
MENU = {
    "1": ("IP lookup", module_ip),
    "2": ("About", module_about),
    "0": ("Exit", None),
}


def main():
    while True:
        clear()
        print(BANNER)
        for key, (label, _) in MENU.items():
            print(f"  {M}[{key}]{RESET} {label}")
        print()
        choice = prompt("select")
        if choice == "0" or choice.lower() in ("q", "quit", "exit"):
            print(f"\n{DIM}bye - ibrahxms | guns.lol/ibrahxm{RESET}\n")
            break
        entry = MENU.get(choice)
        if entry and entry[1]:
            try:
                entry[1]()
            except Exception as e:  # keep the app alive and show what broke
                err(f"{type(e).__name__}: {e}")
                pause()
        else:
            err("invalid option")
            pause()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        input("\ncrashed - press enter to close...")
