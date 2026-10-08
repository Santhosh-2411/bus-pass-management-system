BUS PASS MANAGEMENT SYSTEM

Technologies:
- Python
- Flask
- HTML/CSS
- SQLite

How to run:
1. Open PowerShell in this folder.
2. Create/activate a virtual environment if needed:
   python -m venv venv
   .\venv\Scripts\Activate.ps1
3. Install Flask:
   pip install -r requirements.txt
4. Run:
   python app.py
5. Open the local address shown by Flask in your browser.

The SQLite database file is created automatically when app.py is run.

Current implemented student functions:
- Registration
- Login
- Dashboard
- Apply for Bus Pass
- My Applications
- Check Status
- My Bus Pass
- Logout

Note: The current code does not include an implemented Admin login/approval backend. The documentation may describe admin functionality as a planned/system requirement; do not claim it is implemented unless the backend is added.
