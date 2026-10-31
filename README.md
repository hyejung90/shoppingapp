# 🛒 쇼핑 리스트

아이템을 추가·수정·삭제하고, 산 물건은 체크해서 관리하는 간단한 Streamlit 앱입니다.

## 기능

- **추가**: 이름과 수량을 입력해 목록에 추가 (빈 이름은 거부)
- **수정**: ✏️ 버튼으로 이름·수량 변경 후 저장/취소
- **삭제**: 🗑️ 버튼으로 즉시 삭제
- **체크**: 체크박스로 구매 완료 표시 (취소선)
- **진행 현황**: 완료 개수와 진행률 바
- **완료 항목 삭제**: 체크한 항목 한 번에 삭제

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 http://localhost:8501 로 접속합니다.

## 배포 (Streamlit Community Cloud)

1. 이 저장소를 GitHub에 올립니다.
2. [share.streamlit.io](https://share.streamlit.io)에서 GitHub 계정으로 로그인합니다.
3. **Create app**에서 저장소와 브랜치를 고르고 메인 파일을 `app.py`로 지정한 뒤 배포합니다.

## 참고

- 데이터는 브라우저 세션 동안만 유지됩니다. 새로고침하면 목록이 초기화됩니다.
- 기획 내용은 [PRD.md](PRD.md)를 참고하세요.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `app.py` | 앱 본체 |
| `requirements.txt` | 의존성 (`streamlit`) |
| `.streamlit/config.toml` | 테마 설정 |
| `PRD.md` | 제품 요구사항 문서 |
