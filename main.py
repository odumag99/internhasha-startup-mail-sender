import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # 앱 비밀번호 추천

# 첨부할 파일 경로
ATTACHMENT_PATH = "sample.pdf"  # 예시 파일 (같은 폴더에 있다고 가정)

# 개인화 메일 본문 생성
def create_email_body(name):
    return f"""\
안녕하세요, {name}님.

첨부된 파일을 확인해 주세요.
감사합니다!

- 드림
"""

# CSV 읽고 메일 전송
with open("contacts.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["name"]
        recipient_email = row["email"]

        # 메일 메시지 구성
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = f"{name}님께 드리는 개인화 메일 + 첨부파일"

        # 메일 본문
        body = create_email_body(name)
        msg.attach(MIMEText(body, "plain"))

        # 파일 첨부
        if os.path.exists(ATTACHMENT_PATH):
            with open(ATTACHMENT_PATH, "rb") as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(ATTACHMENT_PATH))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ATTACHMENT_PATH)}"'
                msg.attach(part)
        else:
            print(f"첨부파일을 찾을 수 없습니다: {ATTACHMENT_PATH}")
            continue

        # 메일 전송
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"{name}님에게 메일 전송 완료")
        except Exception as e:
            print(f"{name}님에게 메일 전송 실패: {e}")
