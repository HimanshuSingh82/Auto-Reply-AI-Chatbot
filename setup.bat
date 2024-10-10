@echo off

set "CURRENT_DIR=%Cd%"
set "TARGET_DIR=%CURRENT_DIR%\AutoReplyBot"

git clone https://github.com/HimanshuSingh82/Auto-Reply-AI-Chatbot.git
cd AutoReplyBot
python -m venv myenv
call myenv\Scripts\activate
pip install -r requirements.txt

(
    echo @echo off
    echo cd /d "%TARGET_DIR%"
    echo echo "%TARGET_DIR%"
    echo call myenv\Scripts\activate
    echo python main.py
)> "%CURRENT_DIR%\AutoReplyBot.bat"