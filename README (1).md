# 📚 AI-Powered Library Management System

A smart, command-line Library Management System built with Python — featuring **7 built-in AI/ML algorithms** with **zero external dependencies**. No API keys. No database servers. No pip installs. Just run and go.

\---

## ✨ What Makes This Different

Most library systems are just CRUD apps. This one thinks.

Every book in the collection is a node in a **knowledge graph**. Every shared author or genre is an edge. Three original literary AI engines — **The Ripple**, **The Rabbit Hole**, and **The Silk Road** — use graph algorithms to let readers explore the library in ways no search box ever could.

\---

## 🤖 AI / ML Features

|#|Feature|Algorithm|What It Does|
|-|-|-|-|
|10|🔍 **Smart Fuzzy Search**|Levenshtein Edit Distance|Finds books even with typos — type `"harey poter"`, get Harry Potter|
|11|💡 **Book Recommendations**|Collaborative Filtering|Suggests books based on a member's borrow history and genre affinity|
|12|📊 **Insights Dashboard**|Analytics \& Thresholding|Utilization rate, genre trends, top books, overdue alerts|
|13|⚠️ **Overdue \& Fine Analysis**|Risk Classification|🔴/🟡/🟢 risk levels, projected fines, AI-generated action tips|
|14|🌊 **The Ripple**|BFS|Drop a book — watch related books spread outward in waves|
|15|🐇 **The Rabbit Hole**|DFS (Recursive)|Fall into one obsessive reading chain, as deep as it goes|
|16|🗺️ **The Silk Road**|A\* Search|Finds the smoothest reading path between two literary worlds|

\---

## 🧠 Literary AI Engines — The Innovation

### 🌊 The Ripple *(BFS — Breadth-First Search)*

> \\\*"Every book you love is a stone dropped in still water."\\\*

Drop any book into the library and The Ripple maps how its ideas radiate outward — wave by wave through the knowledge graph. Wave 1 surfaces books directly linked by author or genre. Wave 2 reaches books linked to those. Each wave grows fainter, more distant — but still connected.

* **Algorithm:** Breadth-First Search on the book knowledge graph
* **Graph:** Books as nodes; shared author (weight 1) or shared genre (weight 2) as edges
* **Output:** Tiered waves with bond type (✍️ same author / 📚 same genre / 🔗 linked chain)

### 🐇 The Rabbit Hole *(DFS — Depth-First Search, Recursive)*

> \\\*"You didn't plan to read this many books. But one led to another."\\\*

Chases the strongest link (author) as deep as possible before backtracking to genre links. Visualised as an indented descent — each level deeper in the hole. Reports how far you fell and how many author vs genre links were followed.

* **Algorithm:** Recursive Depth-First Search
* **Priority:** Author links explored first (depth-first into the same author's catalogue)
* **Output:** Indented chain with link type at every step; depth statistics at the end

### 🗺️ The Silk Road *(A\* Search)*

> \\\*"Ancient traders didn't teleport from Rome to China. They traveled through connected cities."\\\*

Finds the optimal (minimum-cost) reading path between any two books using genre-proximity as the heuristic `h(n)`. Guarantees the least-friction route — fewer genre jumps, smoother reading transition. Rates the journey's smoothness (⭐⭐⭐ / ⭐⭐ / ⭐) and explains each waypoint.

* **Algorithm:** A\* Search with admissible genre-distance heuristic
* **Cost:** Author link = 1, Genre link = 2
* **Heuristic h(n):** Pre-defined genre proximity table (e.g. Fiction↔Dystopia = 1, Fantasy↔Sci-Fi = 1)
* **Guarantee:** Optimal path — no shorter route exists

\---

## 🚀 Features Overview

* 📖 **Book Management** — Add, view, search, delete books
* 👤 **Member Management** — Register and view library members
* 🔄 **Issue \& Return** — 14-day loan periods; auto-calculates overdue fines at ₹2/day
* 💾 **SQLite Database** — Lightweight, file-based, zero setup
* 🌱 **Auto-Seeded Data** — 20 sample books across 10 genres, 5 members, pre-loaded on first run

\---

## 🛠️ Setup \& Run

### Prerequisites

* **Python 3.7 or higher**
* No `pip install` needed — every module is part of Python's standard library

### 1\. Check your Python version

```bash
python --version
# or
python3 --version
```

### 2\. Clone the repository

```bash
git clone https://github.com/{your-username}/ai-library-management
cd ai-library-management
```

### 3\. Run

```bash
python main.py
# or on some systems:
python3 main.py
```

The SQLite database (`library.db`) is created automatically on first run with 20 sample books and 5 members pre-loaded. No configuration needed.

\---

## 📁 Project Structure

```
ai-library-management/
│
├── main.py           # CLI entry point — all menus and user interaction
├── database.py       # SQLite database layer — all CRUD operations
├── ai\\\_engine.py      # All 7 AI/ML algorithms
├── requirements.txt  # No external dependencies (standard library only)
├── library.db        # Auto-generated on first run (not committed to git)
└── README.md         # This file
```

\---

## 🎮 How to Use

### Menu Reference

```
1–4   : Book management      (add, view, search, delete)
5–6   : Member management    (add, view)
7–9   : Transactions         (issue, return, view issued)
10    : 🔍  Smart Fuzzy Search
11    : 💡  Book Recommendations
12    : 📊  Insights Dashboard
13    : ⚠️   Overdue \\\& Fine Analysis
14    : 🌊  The Ripple        — BFS book discovery
15    : 🐇  The Rabbit Hole   — DFS reading chain
16    : 🗺️   The Silk Road    — A\\\* optimal reading path
0     : Exit
```

### Recommended Walkthrough

1. `python main.py` — starts with 20 books and 5 members ready
2. **Option 2** — browse the pre-loaded collection
3. **Option 10** — search `"harey poter"` — AI finds Harry Potter despite the typo
4. **Option 11** — enter Member ID `1` — get personalized recommendations
5. **Option 12** — analytics dashboard with genre popularity chart
6. **Option 13** — overdue risk report with projected fines
7. **Option 14** — enter Book ID `6` (Harry Potter) — watch The Ripple spread
8. **Option 15** — enter Book ID `9` (Atomic Habits) — fall down The Rabbit Hole
9. **Option 16** — pick two books from different genres — The Silk Road charts your path

\---

## 📊 Database Schema

```sql
books        (id, title, author, genre, year, copies, available)
members      (id, name, email, phone, joined)
issued\\\_books (id, member\\\_id, book\\\_id, issue\\\_date, due\\\_date, return\\\_date, fine)
```

The knowledge graph is built dynamically in-memory from the `books` table — no graph schema needed in the database.

\---

## 🔧 Resetting the Database

```bash
rm library.db        # Linux / Mac
del library.db       # Windows

python main.py       # Re-seeds automatically on next run
```

\---

## 📝 Technologies Used

|Technology|Purpose|
|-|-|
|Python 3.7+|Core language|
|`sqlite3`|Built-in file-based database|
|`collections.deque`|BFS queue for The Ripple|
|`heapq`|A\* priority queue for The Silk Road|
|Levenshtein Distance|Fuzzy search (custom implementation)|
|Collaborative Filtering|Book recommendations (custom implementation)|
|Recursive DFS|Deep reading chains for The Rabbit Hole|

\---

## 👨‍💻Statement

Built as a college project demonstrating real AI/ML algorithm integration — BFS, DFS, A\*, Levenshtein edit distance, and collaborative filtering — inside a practical, working application, with zero external dependencies.

\---

## 

