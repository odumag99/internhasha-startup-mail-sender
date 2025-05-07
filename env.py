# dotenv 설치하기 귀찮아서 만든 env 보관용 .py
# 주의!! .gitignore에 추가할 것

YOUR_NAME = "홍길동" # 여기에 이름 입력
YOUR_PHONE_NO = "010-1234-6789" # 여기에 전화번호 입력
SENDING_DATE = "2025. 5. 8." # 여기에 보내기 예약 날짜 입력
SENDING_TIME = "오전 10:02" # 여기에 보내기 시간 입력

INTERNHASHA_ONEPAGER_FILE_PATH = "인턴하샤 원페이저.pdf" # main.py와 같은 디렉토리에 '인턴하샤 원페이저.pdf'를 놓아주세요.
MAIL_URL = "https://mail.google.com/mail/u/2/#inbox" # 메일함에 들어간 후 URL을 복사 후후 여기에 붙여넣기 해주세요
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe" # 크롬 실행파일 디렉토리를 찾아서 입력해주세요.

# 이 아래는 크게 건드실 필요 없습니다.
EMAIL_SUBJECT = "서울대 인턴 매칭 플랫폼 ‘인턴하샤’ 채용 공고 수집 문의"
PORT = 1234


# 개인화 메일 본문 생성
def generate_body(name):
    return f"""\
{name} 담당자님, 안녕하세요.

서울대학교 컴퓨터공학부 소속 개발 동아리 와플스튜디오 인턴하샤 팀의 {YOUR_NAME}입니다.

{YOUR_NAME} 드림
전화번호: {YOUR_PHONE_NO}
"""