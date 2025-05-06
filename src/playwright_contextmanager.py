from playwright.sync_api import Playwright, sync_playwright
import atexit
import signal
import sys

PWS = []
PWS_CLEANUP_ENABLED = False

def cleanup_pws():
    """
    PWS들을 모두 cleanup하는 함수
    """
    global PWS
    for pw in PWS:
        pw.stop()
        pw = None

def signal_handler(sig, frame):
    "종료 시그널을 받아 cleanup 실행하는 핸들러"
    cleanup_pws()
    sys.exit(0)

def register_pw_cleanup_at_termination():
    """
    정상 종료 시 cleanup을 register하고, 중도 종료 시 cleanup하는 핸들러 등록록
    """
    # 이미 등록된 경우에는 pass
    global PWS_CLEANUP_ENABLED
    if not PWS_CLEANUP_ENABLED:
        atexit.register(cleanup_pws)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        PWS_CLEANUP_ENABLED = True


def get_playwright() -> Playwright :
    """
    Context가 open된 객체를 반환하고, 종료 시 stop하도록 register하하는 함수
    """
    playwright = sync_playwright().start()
    PWS.append(playwright)
    register_pw_cleanup_at_termination()

    return playwright