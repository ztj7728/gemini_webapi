import asyncio
import os
from pathlib import Path
from typing import Optional

from gemini_webapi import GeminiClient
from dotenv import load_dotenv

ENV_PATH = Path(".env")
load_dotenv(override=False)

SECURE_1PSID = os.getenv("SECURE_1PSID")
SECURE_1PSIDTS = os.getenv("SECURE_1PSIDTS")
if not SECURE_1PSID or not SECURE_1PSIDTS:
    raise RuntimeError("Missing SECURE_1PSID or SECURE_1PSIDTS in .env. Run get_latest_gemini_cookies.py first.")

PROXY = "http://127.0.0.1:15665"  # None if no proxy
CHECK_INTERVAL = 5                # seconds between checks
HEARTBEAT_EVERY = 1               # print dot each interval (set >1 to group)


def _update_env_file(key: str, value: str, env_path: Path = ENV_PATH) -> None:
    """Insert or replace key=value in .env (UTF‑8)."""
    lines, updated = [], False
    if env_path.exists():
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key}="):
                    lines.append(f"{key}={value}\n")
                    updated = True
                else:
                    lines.append(line)
    if not updated:
        lines.append(f"{key}={value}\n")
    env_path.write_text("".join(lines), encoding="utf-8")


def _partner_cookie(jar: dict[str, str]) -> Optional[str]:
    for name in ("__Secure-1PSIDTS", "__Secure-1PSIDCC", "Secure_1PSIDTS", "Secure_1PSIDCC"):
        if name in jar:
            return jar[name]
    return None


async def monitor_cookies(client: GeminiClient, stop_event: asyncio.Event) -> None:
    last = _partner_cookie(client.cookies)
    tick = 0
    while not stop_event.is_set():
        await asyncio.sleep(CHECK_INTERVAL)
        current = _partner_cookie(client.cookies)
        if current and current != last:
            last = current
            os.environ["SECURE_1PSIDTS"] = current
            _update_env_file("SECURE_1PSIDTS", current)
            print(f"\n[auto‑save] Updated .env with new PSIDTS/CC: {current[:36]}…", flush=True)
            tick = 0  # reset after update
        else:
            tick += 1
            if tick % HEARTBEAT_EVERY == 0:
                print(".", end=" ", flush=True)


async def main() -> None:
    client = GeminiClient(SECURE_1PSID, SECURE_1PSIDTS, proxy=PROXY)
    await client.init(timeout=30, auto_close=False, close_delay=300, auto_refresh=True)

    stop_event = asyncio.Event()
    monitor_task = asyncio.create_task(monitor_cookies(client, stop_event))

    try:
        resp = await client.generate_content("What's you language model version? Reply version number only.")
        print(resp.text)

        print("\n[Press Enter to quit]", end="", flush=True)
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, input)
    finally:
        stop_event.set()
        await monitor_task
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
