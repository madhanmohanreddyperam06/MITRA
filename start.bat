@echo off
echo Starting Smart College Helpdesk Bot...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Download spaCy model
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

REM Start backend API in background
echo Starting backend API...
cd backend
start /B python main.py
cd ..

REM Wait for backend to start
timeout /T 5 /NOBREAK

REM Start Streamlit frontend
echo Starting Streamlit frontend...
cd streamlit_app
streamlit run main.py

pause
