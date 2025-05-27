"""
get_latest_gemini_cookies.py
============================

Launches a **Chromium** browser via Playwright (proxy ``http://127.0.0.1:15665``) so you can log in to
https://gemini.google.com/.  After login, it extracts Google account session cookies—**__Secure-1PSID** plus its
companion token (nowadays often **__Secure-1PSIDCC** instead of the older **__Secure-1PSIDTS**).  The two values
are printed and can be written to ``.env``.

Why you saw only ``__Secure-1PSID``
----------------------------------
Google has migrated from the legacy *PSID* + *PSIDTS* pair to **PSID** + **PSIDCC** (cookie suffix *CC* stands for
*Country Code*).  Gemini’s backend accepts either pair, but many tools still look for *PSIDTS* only—hence our
script failed.

What’s fixed
------------
* **New candidates**: now searches for ``__Secure-1PSIDCC`` and ``Secure_1PSIDCC`` as the *TS/CC* partner.
* If *PSID* exists but partner token is missing, we still print *PSID* and warn that you must supply the
  partner cookie manually (DevTools copy‑paste) or upgrade your downstream client.
* Added ``--list`` CLI flag to dump all cookie names even on success.

Prerequisites
-------------
.. code:: bash

   pip install playwright python-dotenv
   playwright install chromium

Usage
-----
.. code:: bash

   python get_latest_gemini_cookies.py            # interactive
   python get_latest_gemini_cookies.py --list      # always list cookie names

Security note: Treat these cookies like passwords—**store securely and rotate periodically**.
"""

import asyncio
import argparse
import os
from pathlib import Path
from typing import Optional, Tuple

from playwright.async_api import async_playwright

# --- Configuration -----------------------------------------------------------
PROXY = "http://127.0.0.1:15665"  # Same proxy used by GeminiClient
SAVE_TO_ENV = True                # Set False to skip writing .env
ENV_PATH = Path(".env")           # Where to write the .env file
# -----------------------------------------------------------------------------

PSID_NAMES = ["__Secure-1PSID", "Secure_1PSID"]
PSID_PARTNER_NAMES = [
    "__Secure-1PSIDTS",  # legacy
    "Secure_1PSIDTS",    # legacy
    "__Secure-1PSIDCC",  # new
    "Secure_1PSIDCC",    # new
]


def _extract_cookie(cookies: list[dict], candidates: list[str]) -> Optional[str]:
    mapping = {c["name"]: c["value"] for c in cookies}
    for name in candidates:
        if name in mapping:
            return mapping[name]
    return None


def _write_env(sid: str, partner: Optional[str]) -> None:
    lines = [f"SECURE_1PSID={sid}"]
    if partner:
        lines.append(f"SECURE_1PSIDTS={partner}")
    content = os.linesep.join(lines) + os.linesep
    ENV_PATH.write_text(content, encoding="utf-8")
    print(f"[+] Saved credentials to {ENV_PATH.resolve()}")


async def fetch_cookies(list_always: bool = False) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, proxy={"server": PROXY})
        context = await browser.new_context()
        page = await context.new_page()
        print("[+] Opening https://gemini.google.com/ …")
        await page.goto("https://gemini.google.com/")
        print("\n>>> 完成登录后回到终端并按回车 (Press <Enter> after login).\n")
        input()

        cookies = await context.cookies(["https://google.com", "https://gemini.google.com"])
        psid = _extract_cookie(cookies, PSID_NAMES)
        partner = _extract_cookie(cookies, PSID_PARTNER_NAMES)

        if list_always or not partner:
            print("\nAll cookie names in context:")
            print(", ".join(sorted({c["name"] for c in cookies})))

        if psid and partner:
            print("\n[✓] Found cookies:")
            print("PSID   =", psid)
            print("PARTNER=", partner)
            if SAVE_TO_ENV:
                _write_env(psid, partner)
        elif psid:
            print("\n[!] Found PSID but no matching PSIDTS/PSIDCC.")
            print("    PSID =", psid)
            print("    → Open DevTools › Application › Cookies and copy the PSIDCC/PSIDTS manually.")
        else:
            print("[!] Failed to locate PSID cookie. Ensure you are logged in.")

        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Google Gemini PSID cookies via Playwright")
    parser.add_argument("--list", action="store_true", help="Always list all cookie names on success")
    args = parser.parse_args()
    asyncio.run(fetch_cookies(list_always=args.list))


if __name__ == "__main__":
    main()
