@echo off
chcp 949 >nul
cd /d "%~dp0"
echo 도서관 대출 웹페이지를 켭니다. 끄려면 이 창에서 Ctrl+C 를 누르세요.
echo 주소: http://localhost:8000
start "" http://localhost:8000
python -m http.server 8000
pause
