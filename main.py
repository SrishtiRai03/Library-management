#!/usr/bin/env python3
"""
AI-Powered Library Management System
======================================
Algorithms: Fuzzy Search (Levenshtein), Collaborative Filtering,
            BFS, DFS, A* (graph-based book relationship search)
No external API or DB server required.
"""

import os
import sys
from datetime import datetime, timedelta
from ai_engine import AIEngine
from database  import Database


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║          📚  AI-Powered Library Management System            ║
║   The Ripple ❧ The Rabbit Hole ❧ The Silk Road  ❧ More     ║
╚══════════════════════════════════════════════════════════════╝
""")

def main_menu():
    print("""
┌──────────────────────────────────────────┐
│              MAIN MENU                   │
├──────────────────────────────────────────┤
│  📖 BOOK MANAGEMENT                      │
│   1.  Add a Book                         │
│   2.  View All Books                     │
│   3.  Search Books (exact)               │
│   4.  Delete a Book                      │
│                                          │
│  👤 MEMBER MANAGEMENT                    │
│   5.  Add a Member                       │
│   6.  View All Members                   │
│                                          │
│  🔄 TRANSACTIONS                         │
│   7.  Issue a Book                       │
│   8.  Return a Book                      │
│   9.  View Issued Books                  │
│                                          │
│  🤖 AI / ML FEATURES                     │
│  10.  🔍 Smart Fuzzy Search              │
│  11.  💡 Book Recommendations            │
│  12.  📊 Insights Dashboard              │
│  13.  ⚠️  Overdue & Fine Analysis        │
│                                          │
│  📜 LITERARY AI ENGINES                  │
│  14.  🌊 The Ripple        [BFS]         │
│  15.  🐇 The Rabbit Hole   [DFS]         │
│  16.  🗺️  The Silk Road    [A*]          │
│                                          │
│   0.  Exit                               │
└──────────────────────────────────────────┘
""")

def main():
    db = Database()
    db.setup()
    db.seed_sample_data()
    ai = AIEngine(db)

    while True:
        clear()
        banner()
        main_menu()
        choice = input("  Enter your choice: ").strip()

        if   choice == '1':  add_book(db)
        elif choice == '2':  view_all_books(db)
        elif choice == '3':  search_books(db)
        elif choice == '4':  delete_book(db)
        elif choice == '5':  add_member(db)
        elif choice == '6':  view_all_members(db)
        elif choice == '7':  issue_book(db)
        elif choice == '8':  return_book(db)
        elif choice == '9':  view_issued_books(db)
        elif choice == '10': ai_smart_search(ai)
        elif choice == '11': ai_recommendations(ai)
        elif choice == '12': ai_insights(ai)
        elif choice == '13': overdue_analysis(ai)
        elif choice == '14': the_ripple(ai)
        elif choice == '15': the_rabbit_hole(ai)
        elif choice == '16': the_silk_road(ai)
        elif choice == '0':
            print("\n  👋 Goodbye!\n")
            sys.exit(0)
        else:
            print("\n  ❌ Invalid choice.")
            input("\n  Press Enter to continue...")


# ─── BOOK MANAGEMENT ──────────────────────────────────────────────

def add_book(db):
    clear()
    print("\n  ── ADD NEW BOOK ──────────────────────\n")
    title  = input("  Title   : ").strip()
    author = input("  Author  : ").strip()
    genre  = input("  Genre   : ").strip()
    year   = input("  Year    : ").strip()
    copies = input("  Copies  : ").strip()
    if not title or not author:
        print("\n  ❌ Title and Author required."); input("\n  Press Enter..."); return
    try:
        year   = int(year)   if year   else None
        copies = int(copies) if copies else 1
    except ValueError:
        print("\n  ❌ Year/Copies must be numbers."); input("\n  Press Enter..."); return
    db.add_book(title, author, genre, year, copies)
    print(f"\n  ✅ '{title}' added!")
    input("\n  Press Enter to continue...")

def view_all_books(db):
    clear()
    print("\n  ── ALL BOOKS ─────────────────────────\n")
    books = db.get_all_books()
    if not books:
        print("  No books found.")
    else:
        print(f"  {'ID':<5} {'Title':<32} {'Author':<22} {'Genre':<16} {'Yr':<6} {'Cop':<4} Avail")
        print("  " + "─"*92)
        for b in books:
            print(f"  {b[0]:<5} {b[1]:<32} {b[2]:<22} {b[3]:<16} {str(b[4]):<6} {b[5]:<4} {b[6]}")
    input("\n  Press Enter to continue...")

def search_books(db):
    clear()
    print("\n  ── SEARCH BOOKS ──────────────────────\n")
    q  = input("  Title / Author / Genre: ").strip()
    rs = db.search_books_exact(q)
    if not rs:
        print("  No results.")
    else:
        print(f"\n  {'ID':<5} {'Title':<32} {'Author':<22} {'Genre':<16} Avail")
        print("  " + "─"*78)
        for b in rs:
            print(f"  {b[0]:<5} {b[1]:<32} {b[2]:<22} {b[3]:<16} {b[6]}")
    input("\n  Press Enter to continue...")

def delete_book(db):
    clear()
    print("\n  ── DELETE BOOK ───────────────────────\n")
    try:    bid = int(input("  Book ID: ").strip())
    except: print("  ❌ Invalid."); input("\n  Press Enter..."); return
    book = db.get_book_by_id(bid)
    if not book:
        print("  ❌ Not found.")
    elif input(f"  Delete '{book[1]}'? (y/n): ").lower() == 'y':
        db.delete_book(bid); print("  ✅ Deleted.")
    else:
        print("  Cancelled.")
    input("\n  Press Enter to continue...")

# ─── MEMBER MANAGEMENT ────────────────────────────────────────────

def add_member(db):
    clear()
    print("\n  ── ADD MEMBER ────────────────────────\n")
    name  = input("  Name  : ").strip()
    email = input("  Email : ").strip()
    phone = input("  Phone : ").strip()
    if not name:
        print("\n  ❌ Name required."); input("\n  Press Enter..."); return
    db.add_member(name, email, phone)
    print(f"\n  ✅ Member '{name}' added!")
    input("\n  Press Enter to continue...")

def view_all_members(db):
    clear()
    print("\n  ── ALL MEMBERS ───────────────────────\n")
    ms = db.get_all_members()
    if not ms:
        print("  No members.")
    else:
        print(f"  {'ID':<5} {'Name':<25} {'Email':<28} {'Phone':<15} Joined")
        print("  " + "─"*85)
        for m in ms:
            print(f"  {m[0]:<5} {m[1]:<25} {m[2]:<28} {m[3]:<15} {m[4]}")
    input("\n  Press Enter to continue...")

# ─── TRANSACTIONS ─────────────────────────────────────────────────

def issue_book(db):
    clear()
    print("\n  ── ISSUE BOOK ────────────────────────\n")
    try:
        mid = int(input("  Member ID : ").strip())
        bid = int(input("  Book ID   : ").strip())
    except:
        print("  ❌ Invalid."); input("\n  Press Enter..."); return
    member = db.get_member_by_id(mid)
    book   = db.get_book_by_id(bid)
    if not member:   print("  ❌ Member not found.")
    elif not book:   print("  ❌ Book not found.")
    elif book[6]<=0: print("  ❌ No copies available.")
    else:
        due = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        db.issue_book(mid, bid, due)
        print(f"\n  ✅ '{book[1]}' issued to {member[1]}")
        print(f"  📅 Due: {due}")
    input("\n  Press Enter to continue...")

def return_book(db):
    clear()
    print("\n  ── RETURN BOOK ───────────────────────\n")
    try:    iid = int(input("  Issue ID: ").strip())
    except: print("  ❌ Invalid."); input("\n  Press Enter..."); return
    result = db.return_book(iid)
    if result is None: print("  ❌ Issue record not found / already returned.")
    elif result > 0:   print(f"\n  ✅ Returned.  ⚠️  Fine: ₹{result:.2f}")
    else:              print("\n  ✅ Returned on time. No fine.")
    input("\n  Press Enter to continue...")

def view_issued_books(db):
    clear()
    print("\n  ── ISSUED BOOKS ──────────────────────\n")
    rows = db.get_issued_books()
    if not rows:
        print("  No books currently issued.")
    else:
        print(f"  {'IssID':<6} {'Member':<20} {'Title':<30} {'Issue':<12} {'Due':<12} Status")
        print("  " + "─"*90)
        today = datetime.now().date()
        for r in rows:
            due    = datetime.strptime(r[4], '%Y-%m-%d').date()
            status = "⚠️ OVERDUE" if due < today else "✅ OK"
            print(f"  {r[0]:<6} {r[1]:<20} {r[2]:<30} {r[3]:<12} {r[4]:<12} {status}")
    input("\n  Press Enter to continue...")

# ─── AI FEATURES ──────────────────────────────────────────────────

def ai_smart_search(ai):
    clear()
    print("\n  ── 🔍 SMART FUZZY SEARCH (Levenshtein) ─────────────────\n")
    print("  Type anything — handles typos, partial words, synonyms.\n")
    q = input("  Your search: ").strip()
    if not q:
        input("\n  Press Enter..."); return
    results = ai.fuzzy_search(q)
    if not results:
        print("\n  No matches found.")
    else:
        print(f"\n  {'ID':<5} {'Title':<32} {'Author':<22} {'Genre':<16} Score")
        print("  " + "─"*80)
        for r in results:
            print(f"  {r['id']:<5} {r['title']:<32} {r['author']:<22} {r['genre']:<16} {r['score']}%")
    input("\n  Press Enter to continue...")

def ai_recommendations(ai):
    clear()
    print("\n  ── 💡 AI BOOK RECOMMENDATIONS (Collaborative Filtering) ─\n")
    try:    mid = int(input("  Member ID: ").strip())
    except: print("  ❌ Invalid."); input("\n  Press Enter..."); return
    member = ai.db.get_member_by_id(mid)
    if not member:
        print("  ❌ Member not found."); input("\n  Press Enter..."); return
    recs = ai.recommend_books(mid)
    print(f"\n  Recommendations for {member[1]}:\n")
    if not recs:
        print("  Not enough history. Issue at least 2-3 books first.")
    else:
        for i, r in enumerate(recs, 1):
            print(f"  {i}. 📖 {r['title']} — {r['author']}")
            print(f"     Genre: {r['genre']}   Reason: {r['reason']}\n")
    input("\n  Press Enter to continue...")

def ai_insights(ai):
    clear()
    print(ai.generate_insights())
    input("\n  Press Enter to continue...")

def overdue_analysis(ai):
    clear()
    print(ai.overdue_report())
    input("\n  Press Enter to continue...")

# ─── LITERARY AI ENGINES ──────────────────────────────────────────

def _pick_book(ai, prompt="  Drop your stone (Book ID): "):
    """Helper: show books list then pick one by ID."""
    books = ai.get_book_list()
    print(f"\n  {'ID':<5} {'Title':<32} {'Author':<22} {'Genre'}")
    print("  " + "─"*75)
    for b in books:
        print(f"  {b[0]:<5} {b[1]:<32} {b[2]:<22} {b[3]}")
    print()
    try:    return int(input(prompt).strip())
    except: return None


# ══════════════════════════════════════════════════════════════════
#  🌊  THE RIPPLE
#
#  Like dropping a stone in still water — one book creates
#  ripples that spread outward through the library's knowledge
#  graph. Wave 1 touches books directly linked by author or genre.
#  Wave 2 reaches books linked to those. Each wave grows fainter,
#  more distant — but still connected.
#
#  Algorithm: Breadth-First Search (BFS)
# ══════════════════════════════════════════════════════════════════

def the_ripple(ai):
    clear()
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   🌊  T H E   R I P P L E                              ║
  ║   Drop a book into the library — watch the waves spread  ║
  ╚══════════════════════════════════════════════════════════╝

  Every book you love is a stone dropped in still water.
  The Ripple maps how that book's ideas, genre, and author
  radiate outward through the entire library — wave by wave.

  ✦ Wave 1  — Books directly linked (same author or genre)
  ✦ Wave 2  — Books linked to those
  ✦ Wave 3  — The outermost reach of influence

  Algorithm: Breadth-First Search (BFS)
  ──────────────────────────────────────────────────────────
""")

    bid = _pick_book(ai, "  Drop your stone — enter Book ID: ")
    if bid is None:
        print("  ❌ Invalid."); input("\n  Press Enter..."); return

    ai._get_graph()
    if bid not in ai._books_map:
        print("  ❌ Book not found."); input("\n  Press Enter..."); return

    stone = ai._books_map[bid]
    print(f"\n  🪨 Your stone: \"{stone[1]}\" by {stone[2]}")
    print(f"     Genre: {stone[3]}")
    print(f"\n  Dropping into the library waters...\n")

    levels = ai.bfs_discover(bid, max_depth=3)

    if not levels:
        print("  The water is still — no ripples found.")
        print("  This book has no genre or author links in the current collection.")
    else:
        wave_labels = {
            1: ("🌊", "FIRST WAVE", "Directly connected — same author or genre"),
            2: ("〰️ ", "SECOND WAVE", "Connected through a shared link"),
            3: ("·  ", "THIRD WAVE",  "The furthest reach — faint but connected"),
        }
        total = 0
        for depth, books in sorted(levels.items()):
            icon, wave_name, description = wave_labels.get(depth, ("·", f"WAVE {depth}", ""))
            total += len(books)
            print(f"  {icon} {wave_name}  —  {description}")
            print(f"  {'─'*58}")
            for b in books:
                # Show what kind of link connects them
                direct_weight = ai._graph.get(bid, {}).get(b['id'])
                if direct_weight == 1:
                    bond = "✍️  same author"
                elif direct_weight == 2:
                    bond = "📚 same genre"
                else:
                    bond = "🔗 linked chain"
                print(f"  │  [{b['id']:>2}] {b['title']:<32} {b['genre']:<16} ← {bond}")
            print(f"  │   {len(books)} book(s) in this wave\n")

        print(f"  ════════════════════════════════════════════════════════")
        print(f"  🌊 The Ripple reached {total} books across {len(levels)} waves.")
        print(f"  💡 The closer the wave, the stronger the reading connection.")

    input("\n\n  Press Enter to continue...")


# ══════════════════════════════════════════════════════════════════
#  🐇  THE RABBIT HOLE
#
#  Alice didn't plan to fall — she just followed one thread
#  deeper and deeper. The Rabbit Hole does the same: starting
#  from one book, it chases the strongest link (same author),
#  then the next, going as deep as the library allows before
#  surfacing for air.
#
#  Algorithm: Depth-First Search (DFS) — Recursive
# ══════════════════════════════════════════════════════════════════

def the_rabbit_hole(ai):
    clear()
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   🐇  T H E   R A B B I T   H O L E                    ║
  ║   Fall in. Follow the thread. See how deep it goes.     ║
  ╚══════════════════════════════════════════════════════════╝

  You didn't plan to read this many books.
  But one led to another. And another. And another.

  The Rabbit Hole follows the deepest possible reading chain
  from your chosen book — author links first (the obsession),
  then genre links (the drift). It never stops until it has
  to surface.

  ✦ 🐇  = Entry point (your book)
  ✦ 📖  = Author-linked (fell deeper — same writer's world)
  ✦ 📗  = Genre-linked (drifted into a neighbouring universe)

  Algorithm: Depth-First Search (DFS) — Recursive
  ──────────────────────────────────────────────────────────
""")

    bid = _pick_book(ai, "  Choose where to fall — enter Book ID: ")
    if bid is None:
        print("  ❌ Invalid."); input("\n  Press Enter..."); return

    ai._get_graph()
    if bid not in ai._books_map:
        print("  ❌ Book not found."); input("\n  Press Enter..."); return

    entry = ai._books_map[bid]
    print(f"\n  🐇 Falling into: \"{entry[1]}\" by {entry[2]}")
    print(f"     Genre: {entry[3]}\n")
    print(f"  THE HOLE  (each level = one link deeper)")
    print(f"  {'─'*60}")

    path = ai.dfs_explore(bid, max_depth=5)

    if not path:
        print("  The hole is shallow — no further connections found.")
    else:
        depth_chars = ["🐇", "📖", "📗", "📘", "📙", "📕"]
        for node in path:
            d      = node['depth']
            indent = "  │  " * d
            icon   = depth_chars[min(d, 5)]
            if d == 0:
                print(f"\n  {icon}  [{node['id']}] \"{node['title']}\"")
                print(f"       by {node['author']}  ({node['genre']})")
                print(f"       ↓ falling...")
            else:
                link_icon = "✍️ " if node['link'] == "Same Author" else "📚"
                print(f"\n  {indent}{icon} [{node['id']}] \"{node['title']}\"")
                print(f"  {indent}     by {node['author']}  ({node['genre']})")
                print(f"  {indent}     {link_icon} {node['link']}")

        max_depth_reached = max(n['depth'] for n in path)
        author_links = sum(1 for n in path if n['link'] == 'Same Author')
        genre_links  = sum(1 for n in path if n['link'] == 'Same Genre')

        print(f"\n  {'─'*60}")
        print(f"  🐇 You fell {max_depth_reached} level(s) deep.")
        print(f"     ✍️  Author links followed : {author_links}")
        print(f"     📚 Genre links followed  : {genre_links}")
        print(f"     📖 Total books visited   : {len(path)}")
        print(f"\n  💡 The deeper the hole, the more obsessive the reading trail.")

    input("\n\n  Press Enter to surface...")


# ══════════════════════════════════════════════════════════════════
#  🗺️  THE SILK ROAD
#
#  Ancient traders didn't teleport from Rome to China.
#  They traveled through connected cities — each one a
#  stepping stone, a bridge between worlds.
#  The Silk Road finds the most elegant, least jarring
#  reading journey between two very different books.
#
#  Algorithm: A* Search
#  Cost:      author link = 1, genre link = 2
#  Heuristic: genre proximity to destination
# ══════════════════════════════════════════════════════════════════

def the_silk_road(ai):
    clear()
    print("""
  ╔══════════════════════════════════════════════════════════╗
  ║   🗺️   T H E   S I L K   R O A D                       ║
  ║   The most elegant path between two literary worlds      ║
  ╚══════════════════════════════════════════════════════════╝

  You are here. You want to be there.
  But the jump feels too large — different genres, different worlds.

  The Silk Road charts the smoothest overland route between
  two books, using connecting titles as waypoints. Like the
  ancient trade routes, it avoids unnecessary detours and
  finds the path of least literary friction.

  ✦ Each waypoint = a book that bridges the gap
  ✦ Author links  = short, smooth passage (cost: 1)
  ✦ Genre links   = a gentle shift in terrain (cost: 2)
  ✦ The route is optimal — A* guarantees no shorter path exists

  Algorithm: A* Search with genre-distance heuristic
  ──────────────────────────────────────────────────────────
""")

    print("  ── YOUR ORIGIN  ────────────────────────────────────────")
    start_id = _pick_book(ai, "  Where does your journey begin? Book ID: ")
    if start_id is None:
        print("  ❌ Invalid."); input("\n  Press Enter..."); return

    print("\n  ── YOUR DESTINATION ────────────────────────────────────")
    goal_id = _pick_book(ai, "  Where do you want to arrive? Book ID: ")
    if goal_id is None:
        print("  ❌ Invalid."); input("\n  Press Enter..."); return

    ai._get_graph()
    if start_id not in ai._books_map or goal_id not in ai._books_map:
        print("  ❌ One or both books not found."); input("\n  Press Enter..."); return
    if start_id == goal_id:
        print("  ℹ️  You're already there!"); input("\n  Press Enter..."); return

    sb = ai._books_map[start_id]
    gb = ai._books_map[goal_id]

    print(f"\n  🏛️  ORIGIN      : \"{sb[1]}\" by {sb[2]}  [{sb[3]}]")
    print(f"  🏯  DESTINATION : \"{gb[1]}\" by {gb[2]}  [{gb[3]}]")
    print(f"\n  Charting the route...\n")

    path = ai.astar_reading_path(start_id, goal_id)

    if path is None:
        print("  ╔══════════════════════════════════════════════════════╗")
        print("  ║  🗺️  No trade route exists between these two worlds. ║")
        print("  ║  These books are literary islands — unconnected      ║")
        print("  ║  by any author or genre bridge in this library.      ║")
        print("  ║                                                      ║")
        print("  ║  💡 Try adding more books to build the connection.   ║")
        print("  ╚══════════════════════════════════════════════════════╝")
    else:
        total_cost = sum(
            ai._graph[path[i-1]['id']].get(path[i]['id'], 0)
            for i in range(1, len(path))
        )
        smoothness = "⭐⭐⭐ Very Smooth" if total_cost <= 2 else \
                     "⭐⭐  Moderate"     if total_cost <= 5 else \
                     "⭐   Some Friction"

        print(f"  ✅ Route found!  Waypoints: {len(path)}   "
              f"Travel cost: {total_cost}   Smoothness: {smoothness}")
        print(f"\n  {'═'*60}")

        terrain_icons = {
            "Same Author": ("✍️ ", "Author connection — smooth, familiar terrain"),
            "Same Genre":  ("📚", "Genre bridge — a gentle shift in landscape"),
            "Start":       ("🏛️ ", "Your origin"),
        }

        for step in path:
            icon, terrain = terrain_icons.get(step['link'], ("·", step['link']))
            is_start = step['step'] == 1
            is_goal  = step['id'] == goal_id

            marker = "🏛️  ORIGIN     " if is_start else \
                     "🏯  DESTINATION" if is_goal  else \
                    f"🏕️  WAYPOINT {step['step']-1:>2} "

            print(f"\n  {marker}  [{step['id']}] \"{step['title']}\"")
            print(f"               by {step['author']}")
            print(f"               Genre: {step['genre']}")
            if not is_start:
                print(f"               {icon} {terrain}")

        print(f"\n  {'═'*60}")
        print(f"\n  🗺️  THE SILK ROAD SUMMARY")
        print(f"  {'─'*44}")
        print(f"  Total waypoints  : {len(path)} book(s)")
        print(f"  Travel cost      : {total_cost} (lower = smoother)")
        print(f"  Journey smoothness: {smoothness}")
        print(f"\n  💡 Read these books in order — each one is a stepping")
        print(f"     stone that makes the next feel natural, not jarring.")
        print(f"     A* guarantees this is the least-friction route possible.")

    input("\n\n  Press Enter to fold the map...")


if __name__ == '__main__':
    main()
