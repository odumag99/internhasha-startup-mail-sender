import subprocess
import requests
import time
from playwright.sync_api import Playwright, sync_playwright

def open_browser(
        chrome_path: str = "C:/Program Files/Google/Chrome/Application/chrome.exe",
        port: str = "7054"
):
    """
    Browser 여는 함수
    """
    subprocess.Popen(f'"{chrome_path}" --user-data-dir="C:/Users/odumag99/Desktop/ChromeUserDir" --remote-debugging-port={port}"')

def is_cdp_ready(port: int = 0
) -> bool :
    """
    CDP 개설 여부 확인하는 함수
    """
    try:
        res = requests.get(f"http://localhost:{port}/json/version")
        if res.status_code == 200:
            return True
        else: return False
    except:
        return False


def wait_until_cdp_ready(
        port:int = 7054,
        interval:int = 3,
        max_iter:int = 10
):
    """
    cdp 개설 때까지 기다리는 함수
    """
    iter_count = 0
    while not is_cdp_ready(port=port) and iter_count <= max_iter:
        iter_count += 1
        time.sleep(interval)

    if not is_cdp_ready(port=port):
        raise Exception("CDP 최대 대기 횟수 초과")


