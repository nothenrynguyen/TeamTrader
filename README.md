TeamTrader
A Django + Tailwind web app for validating NHL trades based on salary cap, roster rules, and retained salary limits.

🚀 Features
Trade Validation — Checks trades against NHL salary cap and roster rules.

Data Models — Teams, Contracts, Draft Picks, and Retained Salaries.

CSV Data Loaders — Easily import NHL roster and contract information.

Responsive UI — Built with Tailwind CSS for clean and fast styling.

📦 Getting Started
1️⃣ Clone the repository
bash
Copy
Edit
git clone https://github.com/nothenrynguyen/TeamTrader.git
cd TeamTrader
2️⃣ Set up a virtual environment
bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Apply migrations
bash
Copy
Edit
python manage.py migrate
5️⃣ Load NHL data
bash
Copy
Edit
python manage.py load_data
python manage.py load_retention trades\data\retention_used.csv
6️⃣ Start the development server
bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

📂 Project Structure
bash
Copy
Edit
TeamTrader/
│
├── trades/                     # App for teams, contracts, picks, retention
│   ├── data/                    # CSV data files
│   ├── management/commands/     # Data loading scripts
│   └── models.py                 # Database models
│
├── templates/                   # HTML templates
├── static/                      # CSS & JS files
├── tradebot/                    # Django project config
└── README.md
🛠 Tech Stack
Backend — Django

Frontend — Tailwind CSS

Database — SQLite (default, easily swappable)

Other Tools — Python, Django ORM