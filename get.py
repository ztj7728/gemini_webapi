import asyncio
import argparse
import os
from pathlib import Path
from typing import Optional, Tuple

from playwright.async_api import async_playwright

# --- Configuration -----------------------------------------------------------
PROXY = "http://127.0.0.1:15665"  # Same proxy used by GeminiClient
SAVE_TO_ENV = True              # Set False to skip writing .env
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
    """
    Extracts the first matching cookie value from a list of cookies.

    Args:
        cookies: A list of cookie dictionaries (from Playwright).
        candidates: A list of cookie names to search for, in order of preference.

    Returns:
        The value of the first matching cookie found, or None if no match.
    """
    mapping = {c["name"]: c["value"] for c in cookies}
    for name in candidates:
        if name in mapping:
            return mapping[name]
    return None


def _write_env(sid: str, partner: Optional[str]) -> None:
    """
    Updates PSID and partner cookie values in an existing .env file.
    If the .env file does not exist, it prints a message and does nothing.
    If keys are not found in the file, they are not added.

    Args:
        sid: The __Secure-1PSID cookie value.
        partner: The __Secure-1PSIDTS or __Secure-1PSIDCC cookie value, or None.
    """
    # 检查 .env 文件是否存在
    if not ENV_PATH.exists():
        print(f"[!] {ENV_PATH.resolve()} 文件未找到。Cookie 未保存。")
        return

    try:
        # 读取 .env文件的所有行
        original_lines = ENV_PATH.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        print(f"[!] 读取 {ENV_PATH.resolve()} 文件失败: {e}")
        return

    updated_lines = []
    key_psid_found_in_file = False
    key_partner_found_in_file = False
    
    # 标记是否有实际的值更改，以便决定是否真的需要写入文件
    actual_content_changed = False

    for line in original_lines:
        stripped_line = line.strip()
        if stripped_line.startswith("SECURE_1PSID="):
            key_psid_found_in_file = True
            new_line_content = f"SECURE_1PSID={sid}"
            if line != new_line_content:
                actual_content_changed = True
            updated_lines.append(new_line_content)
        elif stripped_line.startswith("SECURE_1PSIDTS="):
            key_partner_found_in_file = True
            if partner is not None:
                new_line_content = f"SECURE_1PSIDTS={partner}"
                if line != new_line_content:
                    actual_content_changed = True
                updated_lines.append(new_line_content)
            else:
                # 如果本次没有获取到 partner cookie，保留 .env 文件中原有的 SECURE_1PSIDTS 值
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    # 只有当相关键在文件中找到时，才考虑写入或报告状态
    if key_psid_found_in_file or key_partner_found_in_file:
        if actual_content_changed:
            try:
                content_to_write = os.linesep.join(updated_lines)
                if updated_lines:  # 确保在有内容时添加末尾的换行符
                    content_to_write += os.linesep
                ENV_PATH.write_text(content_to_write, encoding="utf-8")
                print(f"[+] {ENV_PATH.resolve()} 文件中的相关 Cookie 值已更新。")
            except Exception as e:
                print(f"[!] 写入 {ENV_PATH.resolve()} 文件失败: {e}")
        else:
            print(f"[i] {ENV_PATH.resolve()} 文件中的相关 Cookie 值已是最新，未作更改。")

        # 如果某些键期望被更新但未在文件中找到 (这种情况不应发生，因为我们基于 key_..._found_in_file)
        # 但为了完整性，可以检查 sid 是否提供了但 key_psid_found_in_file 为 false
        if not key_psid_found_in_file: # 逻辑上，如果执行到这里，这个条件不应为真
             print(f"[!] 提示: 本次提供了 SECURE_1PSID，但该键未在 {ENV_PATH.resolve()} 文件中找到。")
        
        if partner is not None and not key_partner_found_in_file: # 逻辑上，如果执行到这里，这个条件不应为真
             print(f"[!] 提示: 本次提供了 PARTNER cookie，但 SECURE_1PSIDTS 键未在 {ENV_PATH.resolve()} 文件中找到。")
        elif partner is None and key_partner_found_in_file:
             print(f"[i] 信息: 本次未获取到 PARTNER cookie，{ENV_PATH.resolve()} 文件中的 SECURE_1PSIDTS 值未更改。")

    else:
        # 如果 .env 文件存在，但没有包含 SECURE_1PSID 或 SECURE_1PSIDTS 键
        print(f"[i] {ENV_PATH.resolve()} 文件中未找到 SECURE_1PSID 或 SECURE_1PSIDTS 键。文件未作更改。")


async def fetch_cookies(list_always: bool = False) -> None:
    """
    Launches a browser, navigates to Gemini, and attempts to extract
    PSID and PSIDTS/PSIDCC cookies after user login.
    """
    async with async_playwright() as p:
        # Launch browser with proxy settings
        browser = await p.chromium.launch(headless=False, proxy={"server": PROXY})
        context = await browser.new_context()
        page = await context.new_page()

        print("[+] Opening https://gemini.google.com/ …")
        await page.goto("https://gemini.google.com/")

        # Prompt user to log in
        print("\n>>> 完成登录后回到终端并按回车 (Press <Enter> after login).\n")
        input()  # Wait for user to press Enter

        # Get cookies from relevant domains
        cookies = await context.cookies(["https://google.com", "https://gemini.google.com"])

        # Extract the required cookies
        psid = _extract_cookie(cookies, PSID_NAMES)
        partner = _extract_cookie(cookies, PSID_PARTNER_NAMES)

        # List all cookie names if requested or if partner cookie is missing
        if list_always or (psid and not partner): # 如果psid存在但partner缺失，也列出所有cookie帮助调试
            print("\nAll cookie names in context:")
            print(", ".join(sorted({c["name"] for c in cookies})))

        if psid: # 只要psid获取到了就尝试保存或报告
            print("\n[✓] Found PSID cookie.")
            print("PSID    =", psid)
            if partner:
                print("PARTNER =", partner)
            else:
                print("[!] PARTNER cookie (PSIDTS/PSIDCC) not found this time.")
            
            if SAVE_TO_ENV:
                _write_env(psid, partner)
        else:
            print("[!] Failed to locate PSID cookie. Ensure you are logged in.")
            print("    未能定位到 PSID cookie，请确保您已登录。")


        await browser.close()


def main() -> None:
    """
    Parses command-line arguments and runs the cookie fetching process.
    """
    parser = argparse.ArgumentParser(description="Fetch Google Gemini PSID cookies via Playwright")
    parser.add_argument(
        "--list",
        action="store_true",
        help="Always list all cookie names found, even on success"
    )
    args = parser.parse_args()
    asyncio.run(fetch_cookies(list_always=args.list))


if __name__ == "__main__":
    main()
