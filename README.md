# Library-management
# 📚 AI-Powered Library Management System

A smart, command-line Library Management System built with Python — featuring **built-in AI capabilities** with **zero external dependencies**. No API keys. No database servers. Just run and go.

---

## 🤖 AI Features

| Feature | Description |
|---|---|
| 🔍 **Smart Fuzzy Search** | Find books even with typos using Levenshtein edit-distance algorithm |
| 💡 **Book Recommendations** | Personalized suggestions based on member borrow history (collaborative filtering) |
| 📊 **Insights Dashboard** | Auto-generated analytics: utilization rate, genre popularity, borrowing trends |
| ⚠️ **Overdue & Fine Analysis** | Risk-level flagging, fine prediction, and AI-powered actionable suggestions |

---

## 🚀 Features Overview

- 📖 **Book Management** — Add, view, search, delete books
- 👤 **Member Management** — Register and view library members
- 🔄 **Issue & Return** — Issue books with 14-day due dates; auto-calculate overdue fines (₹2/day)
- 💾 **SQLite Database** — Lightweight file-based storage, no setup required
- 🌱 **Auto Seeded Data** — 20 sample books & 5 members pre-loaded on first run

---

## 🛠️ Setup & Run

### Prerequisites
- Python **3.7 or higher**
- No pip installs needed — all modules are part of Python's standard library

### Check Python version
```bash
python --version
# or
python3 --version
```

### Clone the repository
```bash
git clone https://github.com/{your-username}/ai-library-management
cd ai-library-management
```

### Run the application
```bash
python main.py
# or on some systems:
python3 main.py
```

That's it! The database (`library.db`) is created automatically on first run with sample data.

---

## 📁 Project Structure

```
ai-library-management/
│
├── main.py           # Entry point — CLI menus and user interaction
├── database.py       # SQLite database layer (CRUD operations)
├── ai_engine.py      # All AI features (search, recommendations, insights)
├── requirements.txt  # No external dependencies (documents built-ins used)
├── library.db        # Auto-generated SQLite database (created on first run)
└── README.md         # This file
```

---

## 🎮 How to Use

### Main Menu Options
```
1–4   : Book management (add, view, search, delete)
5–6   : Member management (add, view)
7–9   : Transactions (issue, return, view issued)
10    : 🔍 AI Smart Search — typo-tolerant fuzzy search
11    : 💡 AI Book Recommendations — personalized suggestions
12    : 📊 AI Insights Dashboard — library analytics
13    : ⚠️  Overdue & Fine Analysis — risk assessment
0     : Exit
```

### Quick Walkthrough
1. Run `python main.py`
2. Try **Option 2** to see pre-loaded books
3. Try **Option 10** and search `"harey poter"` — AI finds Harry Potter despite typos!
4. Try **Option 11**, enter Member ID `1` — get personalized recommendations
5. Try **Option 12** for a full analytics dashboard
6. Try **Option 13** for overdue fine analysis

---

## 🧠 AI Implementation Details

### 1. Fuzzy Search (`ai_engine.py → fuzzy_search`)
- **Algorithm**: Levenshtein Edit Distance
- Tokenizes query into words, computes edit distance to each word in book metadata
- Books with ≥70% similarity score are returned, ranked by match confidence
- Also includes synonym expansion (`sci-fi → science fiction`, `coding → computer sci`, etc.)

### 2. Book Recommendations (`ai_engine.py → recommend_books`)
- **Algorithm**: Content-Based Collaborative Filtering
- Analyzes member's borrow history to compute **genre affinity scores**
- Recommends unread books in preferred genres, ranked by affinity percentage
- Explains each recommendation with a human-readable reason

### 3. Insights Dashboard (`ai_engine.py → generate_insights`)
- Aggregates real-time stats: utilization rate, genre popularity bars, top books
- Generates **natural-language AI notes** based on thresholds (e.g., high utilization → acquisition alert)
- Overdue summary with top offenders highlighted

### 4. Overdue & Fine Analysis (`ai_engine.py → overdue_report`)
- Classifies each overdue record into **🔴 HIGH / 🟡 MED / 🟢 LOW** risk
- Calculates projected fines (₹2 per overdue day)
- Provides actionable AI suggestions based on average overdue duration

---

## 📊 Database Schema

```sql
books (id, title, author, genre, year, copies, available)
members (id, name, email, phone, joined)
issued_books (id, member_id, book_id, issue_date, due_date, return_date, fine)
```

---

## 🔧 Resetting the Database

To start fresh (clear all data):
```bash
# Delete the auto-generated database file
rm library.db       # Linux/Mac
del library.db      # Windows

# Then re-run the app — it will re-seed sample data
python main.py
```

---

## 📝 Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.7+ | Core language |
| SQLite3 | Built-in database (no server needed) |
| datetime | Due date & fine calculation |
| re (regex) | Query tokenization for AI search |
| Custom Levenshtein | Fuzzy matching algorithm |
| Collaborative Filtering | Recommendation engine |

---

## 👨‍💻 Author

Built as a college project demonstrating AI integration in a real-world management system — without relying on any external AI APIs or services.

---

## 📄 License

MIT License — free to use and modify.
