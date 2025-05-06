import csv
import os
from src.cdp_opener import open_browser, wait_until_cdp_ready
from src.playwright_contextmanager import get_playwright
from env import *


def main():
    # 매크로가 실행될 browser 실행
    open_browser(
        chrome_path = CHROME_PATH,
        port=PORT
    )

    # Chrome DevTools Protocol 정상 가동 여부 확인
    try:
        wait_until_cdp_ready(port=PORT, interval=3, max_iter=10)
    except Exception as e:
        print("CDP 최대 대기 횟수 초과")
        raise e
    print("CDP 정상 작동")

    # CDP에 playwright 연결
    pw = get_playwright()
    browser = pw.chromium.connect_over_cdp(f"http://localhost:{PORT}/", timeout=10000)
    print("지금 열린 페이지에서 인턴하샤 메일함에 들어간 후 Enter를 누르세요.")
    input()
    page = browser.contexts[0].pages[0]
    page.pause()

    # 매크로 실행
    # CSV 읽기
    with open("contacts.csv", newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # 각 수신자별 메일 작성 매크로 실행행
        for row in reader:
            recipient_name = row["name"]
            recipient_email = row["email"]
            print(f"{recipient_name}({recipient_email})에 대한 이메일을 작성하려면 Enter 키를 누르세요.")
            input()

            # 편지쓰기 창 열기
            page.get_by_role("button", name="편지쓰기").click()

            # 수신자 입력
            page.get_by_role("combobox", name="수신자").click()
            page.get_by_role("combobox", name="수신자").fill(recipient_email)
            page.get_by_role("combobox", name="수신자").press("Enter")

            # 제목 입력
            page.get_by_role("textbox", name="제목").click()
            page.get_by_role("textbox", name="제목").fill(EMAIL_SUBJECT)

            # 본문 입력
            # 본문 내용 생성
            body = generate_body(recipient_name)
            page.get_by_role("textbox", name="메일 본문").fill(body)

            # 파일 첨부
            with page.expect_file_chooser() as fc_info:
                page.get_by_role("button", name="파일 첨부").click()
            file_chooser = fc_info.value
            file_chooser.set_files(os.path.abspath(INTERNHASHA_ONEPAGER_FILE_PATH))
            # 파일 업로드 대기
            try:
                progress_bar = page.get_by_role("progressbar", name=f"{os.path.basename(INTERNHASHA_ONEPAGER_FILE_PATH)} 업로드 중")
                progress_bar.wait_for(state="hidden", timeout=30000)
            except Exception as e:
                print("원페이저 업로드 실패")
                page.pause()
                raise e

            # 보내기 예약
            page.get_by_role("button", name="보내기 옵션 더보기").click()
            page.get_by_text("보내기 예약", exact=True).click()
            page.get_by_text("날짜 및 시간 선택").click()
            page.get_by_role("textbox", name="날짜").click()
            page.get_by_role("textbox", name="날짜").fill(SENDING_DATE)
            page.get_by_role("textbox", name="시간").click()
            page.get_by_role("textbox", name="시간").fill(SENDING_TIME)
            page.get_by_role("button", name="보내기 예약").click()

main()