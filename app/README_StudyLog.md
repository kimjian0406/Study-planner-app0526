# 📚 StudyLog – 공부 플래너 웹 애플리케이션

**StudyLog**는 사용자의 공부 계획과 시간을 효과적으로 관리하고 분석할 수 있도록 설계된 웹 기반 공부 플래너입니다.  
실시간 타이머 기능과 통계를 통해 자기주도 학습을 돕는 도구로 활용할 수 있습니다.

---

## ✨ 주요 기능

- 🔐 **회원가입 / 로그인**: 이메일 기반 인증, JWT 사용
- 🗓️ **공부 계획 관리**: 계획 등록, 수정, 삭제 기능
- ⏱️ **공부 타이머**: 실시간 타이머 기록, 일시정지 및 종료 기능
- 📈 **통계 기능**: 일별 / 주별 누적 공부 시간 제공
- ✅ **완료 체크**: 완료된 공부 계획 표시 기능
- 🔒 **보안 고려**: 비밀번호 해싱, 입력 검증, 에러 처리

---

## 🛠️ 사용 기술 스택

| 영역       | 기술                                   |
|------------|----------------------------------------|
| 백엔드     | Python, Flask                          |
| 인증       | JWT (Flask-JWT-Extended)               |
| 데이터베이스 | SQLite (개발), PostgreSQL (배포 가능) |
| ORM        | SQLAlchemy                             |
| 문서화     | Markdown, Postman                      |
| 배포       | GitHub 기반 로컬 실행                  |

---

## 🗂️ 폴더 구조

```
studylog/
├── app/
│   ├── routes/      # API 라우터
│   ├── models/      # 데이터베이스 모델
│   ├── schemas/     # 요청/응답 스키마
│   └── utils/       # JWT, 헬퍼 함수
├── tests/           # 테스트 코드
├── .env             # 환경 변수
├── requirements.txt # 패키지 목록
├── README.md
└── run.py           # 실행 파일
```

---

## ⚙️ 설치 및 실행 방법

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/studylog.git
cd studylog

# 2. 가상환경 생성 및 패키지 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 서버 실행
python run.py
```

---

## 📮 간단한 API 요약

| Method | Endpoint           | 설명                 |
|--------|--------------------|----------------------|
| POST   | /users/signup      | 회원가입             |
| POST   | /users/login       | 로그인 (JWT 발급)    |
| GET    | /plans             | 공부 계획 목록 조회  |
| POST   | /plans             | 공부 계획 생성       |
| PUT    | /plans/{id}        | 공부 계획 수정       |
| DELETE | /plans/{id}        | 공부 계획 삭제       |
| GET    | /statistics/daily  | 일간 공부 시간 통계  |

---

## 📑 관련 문서

- [요구사항 정의서](./01_StudyLog_요구사항_정의서.txt)
- [API 명세서](./02_API_명세서.txt)
- [ERD 설명](./03_ERD_설명.txt)
- [테이블 정의서](./04_테이블_정의서.txt)
- [화면 명세서](./05_화면_명세서.txt)
- [데일리 스크럼 (5/23~5/30)](./스크럼_2025_05_23.txt)

---

## 👤 개발자 정보

- **이름**: [홍길동]
- **GitHub**: [https://github.com/yourusername](https://github.com/yourusername)
- **Email**: [your.email@example.com]

---

> 꾸준한 공부를 위한 첫 걸음, StudyLog와 함께하세요.