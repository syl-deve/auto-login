## Relevant Files

- `C:\work-cloit\auto-login\main.py` - 자동 로그인 로직을 실행하는 메인 파이썬 스크립트입니다.
- `C:\work-cloit\auto-login\config.json` - 로그인 URL, 계정 정보, 타겟 페이지 등 설정을 저장하는 파일입니다.
- `C:\work-cloit\auto-login\requirements.txt` - `selenium` 등 필요한 파이썬 라이브러리를 명시하는 파일입니다.
- `C:\work-cloit\auto-login\.gitignore` - `venv`, `__pycache__`, `config.json` 등 버전 관리에서 제외할 파일을 지정합니다.

### Notes

- 이 프로젝트는 `uv`를 사용하여 파이썬 가상 환경 및 패키지를 관리합니다. `uv`가 설치되어 있지 않다면, `pip install uv` 명령어로 설치해주세요.
- `uv venv` 명령어로 가상환경을 생성하고, `.venv\Scripts\activate` (Windows) 또는 `source .venv/bin/activate` (macOS/Linux)로 활성화합니다.
- `uv pip install -r requirements.txt` 명령어를 사용하여 필요한 라이브러리를 설치합니다.

## Tasks

- [x] 1.0 프로젝트 환경 설정 및 기본 구조 생성
  - [x] 1.1 `uv`를 사용하여 Python 가상 환경 생성 (`uv venv`)
  - [x] 1.2 `requirements.txt` 파일 생성 및 `selenium` 라이브러리 추가
  - [x] 1.3 `uv pip install -r requirements.txt`를 실행하여 라이브러리 설치
  - [x] 1.4 `config.json` 설정 파일의 기본 구조 생성 (login_url, username, password 등)
  - [x] 1.5 `.gitignore` 파일 생성하여 `venv`, `__pycache__`, `config.json` 등 제외
  - [x] 1.6 `main.py` 기본 파일 생성 및 설정 파일 로드 로직 추가

- [x] 2.0 웹 브라우저 제어 및 기본 로그인 구현
  - [x] 2.1 `main.py`에 Selenium WebDriver 초기화 로직 추가
  - [x] 2.2 `config.json`에서 로그인 URL을 읽어 해당 페이지로 이동하는 기능 구현
  - [x] 2.3 `config.json`에 아이디/비밀번호 필드 및 제출 버튼의 CSS selector 추가
  - [x] 2.4 `config.json`의 정보를 사용하여 웹페이지에 아이디/비밀번호를 입력하고 제출하는 기능 구현

- [x] 3.0 OTP 인증 처리 기능 구현
  - [x] 3.1 `config.json`에 OTP 입력 필드 및 제출 버튼의 CSS selector 추가
  - [x] 3.2 아이디/비밀번호 제출 후 OTP 입력 페이지가 나타날 때까지 대기하는 로직 추가
  - [x] 3.3 터미널을 통해 사용자에게 OTP 번호를 입력받는 기능 구현
  - [x] 3.4 입력받은 OTP를 웹페이지에 입력하고 제출하는 기능 구현

- [ ] 4.0 로그인 후처리 및 예외/재시도 로직 구현
  - [ ] 4.1 로그인 성공 여부를 판단하는 로직 구현 (예: 특정 요소 확인)
  - [ ] 4.2 로그인 실패 시, `config.json`에 정의된 횟수와 간격에 따라 재시도하는 로직 구현
  - [ ] 4.3 모든 재시도 실패 시, 오류 메시지를 출력하고 스크립트를 종료하는 로직 구현
  - [ ] 4.4 (추후 구현) 로그인 성공 시, `config.json`에 정의된 타겟 페이지로 이동하는 기능 추가

- [ ] 5.0 코드 정리 및 최종화
  - [ ] 5.1 코드 가독성 향상을 위한 주석 추가 및 리팩토링
  - [ ] 5.2 사용자가 자신의 설정을 쉽게 할 수 있도록 `config.json.example` 파일 생성
  - [ ] 5.3 스크립트 설치, 설정, 실행 방법을 안내하는 `README.md` 파일 작성
  - [ ] 5.4 최종 테스트 및 불필요한 코드/파일 제거