# TeamTrader  
A Django + Tailwind web app for validating NHL trades based on salary cap, roster rules, and retained salary limits.

---

## 🚀 Features  
- **Trade Validation** — Checks trades against NHL salary cap, roster rules, and retained salary limits.  
- **Interactive Frontend** — Select teams, choose players/picks/retention, and validate trades live — no page reloads.  
- **Smart Autocomplete** — Clean input for team selection with real-time suggestions.  
- **Detailed Results** — Clear validation messages: green for valid trades, red with errors for invalid ones.  
- **Data Models** — Teams, Contracts, Draft Picks, and Retained Salaries.  
- **CSV Data Loaders** — Import full NHL roster and contract info from provided files.  
- **Responsive UI** — Built with Tailwind CSS for fast, modern design.  

---

## 🧪 Testing

To confirm the trade validator is working:

- Try submitting a trade with no players/picks selected — it should return an error.
- Try selecting the same team on both sides — the frontend will prevent it.
- All validation happens via a POST request to `/validate/`, returning JSON responses.

---

## 📦 Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/nothenrynguyen/TeamTrader.git
cd TeamTrader
```

### 2️⃣ Set up a virtual environment  
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply migrations  
```bash
python manage.py migrate
```

### 5️⃣ Load NHL data  
```bash
python manage.py load_data
python manage.py load_retention trades\data\retention_used.csv
```

### 6️⃣ Start the development server  
```bash
python manage.py runserver
```

Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.  

---

## 📂 Project Structure  
```text
TeamTrader/
│
├── trades/                     # App for teams, contracts, picks, retention
│   ├── data/                    # CSV data files
│   ├── management/commands/     # Data loading scripts
│   └── models.py                # Database models
│
├── templates/                   # HTML templates
├── static/                      # CSS & JS files
├── tradebot/                    # Django project config
└── README.md
```

---

## 🛠 Tech Stack  
- **Backend** — Django  
- **Frontend** — Tailwind CSS  
- **Database** — SQLite 
- **Other Tools** — Python, Django ORM  


