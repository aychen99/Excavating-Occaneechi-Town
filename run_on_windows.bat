echo "Setting up venv... ..."
if not exist ./venv (
    python -m venv ./venv
)
call ./venv/Scripts/activate.bat
echo "Installing required Python packages... ..."
pip install -r requirements.txt
python run_extraction_and_generation.py
echo "Finished extracting and generating. Press enter to continue... ..."
pause
