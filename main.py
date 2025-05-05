import smtplib
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from env import *

# SMTP 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = INTERNHASHA_EMAIL
EMAIL_PASSWORD = INTERNHASHA_PW 

# 첨부할 파일 경로
ATTACHMENT_PATH = "인턴하샤 원페이저.pdf"  # 예시 파일 (같은 폴더에 있다고 가정)

# CSV 읽고 메일 전송
with open("contacts.csv", newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    # 각 수신자 별 메일 전송
    for row in reader:
        name = row["name"]
        recipient_email = row["email"]

        # 메일 메시지 구성
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = f"서울대 인턴 매칭 플랫폼 ‘인턴하샤’ 채용 공고 수집 문의"

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
            print(f"{recipient_email}에게 보낼 메일을 작성하는 중 첨부파일을 찾지 못했습니다: {ATTACHMENT_PATH}")
            continue

        # 최종 확인
        print(f"""
아래와 같이 메일을 보내시겠습니까?(진행하려면 Enter)
수신자: {msg['To']}({row['name']})
제목: {msg['Subject']}
첨부파일: {msg["Content-Disposition"]}
내용:
{msg["body"]}""")
        input()

        # 메일 전송
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
                print(f"{name}님에게 메일 전송 완료")
        except Exception as e:
            print(f"{name}님에게 메일 전송 실패: {e}")
