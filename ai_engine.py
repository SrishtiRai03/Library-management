"""
ai_engine.py — AI/ML Engine for Library Management System
===========================================================
Algorithms implemented:
  1.  Fuzzy Search         — Levenshtein edit distance
  2.  Recommendations      — Collaborative filtering
  3.  Insights Dashboard   — Analytics & summaries
  4.  Overdue Analysis     — Fine prediction & risk flags

  GRAPH-BASED AI (NEW):
  5.  BFS Discovery        — Level-by-level book relationship exploration
  6.  DFS Explorer         — Deep reading chain traversal
  7.  A* Optimal Path      — Shortest genre-jump reading path between books
"""

from datetime import datetime
from collections import deque
import heapq
import re


class AIEngine:
    def __init__(self, db):
        self.db        = db
        self._graph    = None
        self._books_map = None

    # ══════════════════════════════════════════════════════════════
    #  KNOWLEDGE GRAPH
    #  Nodes = Books,  Edges = shared genre (w=2) or author (w=1)
    # ══════════════════════════════════════════════════════════════

    def build_knowledge_graph(self):
        """Build adjacency-list graph from all books in the library."""
        books          = self.db.get_all_books()
        self._books_map = {b[0]: b for b in books}
        self._graph    = {b[0]: {} for b in books}

        for i, b1 in enumerate(books):
            for j, b2 in enumerate(books):
                if i >= j:
                    continue
                id1, id2   = b1[0], b2[0]
                genre1     = (b1[3] or '').lower()
                genre2     = (b2[3] or '').lower()
                auth1      = (b1[2] or '').lower()
                auth2      = (b2[2] or '').lower()

                if auth1 == auth2 and auth1:       # Same author — very strong
                    self._graph[id1][id2] = 1
                    self._graph[id2][id1] = 1
                elif genre1 == genre2 and genre1:  # Same genre — medium
                    self._graph[id1][id2] = 2
                    self._graph[id2][id1] = 2

        return self._graph

    def _get_graph(self):
        if self._graph is None:
            self.build_knowledge_graph()
        return self._graph

    def get_book_list(self):
        self._get_graph()
        return list(self._books_map.values())

    # ══════════════════════════════════════════════════════════════
    #  5. BFS — Breadth-First Search Book Discovery
    #
    #  WHAT IT DOES:
    #    Starting from one book, explores the knowledge graph
    #    level by level (hop 1 = directly related, hop 2 = related
    #    to related, etc.).  Shows ALL books reachable within N hops.
    #
    #  LIBRARY USE:
    #    "I liked this book — show me what else is related, and how
    #     far they are from my starting point."
    # ══════════════════════════════════════════════════════════════

    def bfs_discover(self, start_book_id, max_depth=3):
        """
        BFS from start_book_id through the book knowledge graph.
        Returns dict: { hop_level: [book_info, ...] }
        """
        graph = self._get_graph()

        if start_book_id not in graph:
            return {}

        visited = {start_book_id}
        queue   = deque([(start_book_id, 0)])
        levels  = {}

        while queue:
            node, depth = queue.popleft()
            if depth > max_depth:
                break
            if depth > 0:
                b    = self._books_map[node]
                levels.setdefault(depth, []).append({
                    'id':     node,
                    'title':  b[1],
                    'author': b[2],
                    'genre':  b[3],
                })
            for neighbour in graph[node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, depth + 1))

        return levels

    # ══════════════════════════════════════════════════════════════
    #  6. DFS — Depth-First Search Reading Chain
    #
    #  WHAT IT DOES:
    #    Dives as deep as possible along one chain of related books
    #    before backtracking — follows author links first (strongest),
    #    then genre links.
    #
    #  LIBRARY USE:
    #    "Show me a deep reading journey: start here and go as far
    #     as possible into related books."
    # ══════════════════════════════════════════════════════════════

    def dfs_explore(self, start_book_id, max_depth=4):
        """
        DFS traversal from start_book_id.
        Returns ordered list of books in traversal order with depth/link info.
        """
        graph = self._get_graph()

        if start_book_id not in graph:
            return []

        visited = set()
        path    = []

        def _dfs(node, depth, link_label):
            if depth > max_depth or node in visited:
                return
            visited.add(node)
            b = self._books_map[node]
            path.append({
                'depth':  depth,
                'id':     node,
                'title':  b[1],
                'author': b[2],
                'genre':  b[3],
                'link':   link_label,
            })
            # Author links (weight=1) explored before genre links (weight=2)
            neighbours = sorted(graph[node].items(), key=lambda x: x[1])
            for nbr, w in neighbours:
                _dfs(nbr, depth + 1, "Same Author" if w == 1 else "Same Genre")

        _dfs(start_book_id, 0, "Start")
        return path

    # ══════════════════════════════════════════════════════════════
    #  7. A* — Optimal Reading Path Between Two Books
    #
    #  WHAT IT DOES:
    #    Finds the minimum-cost path through the knowledge graph
    #    from book A to book B.
    #    g(n) = cumulative edge cost (author=1, genre=2)
    #    h(n) = genre-distance heuristic to goal book's genre
    #
    #  LIBRARY USE:
    #    "I want to transition from reading Fantasy to Computer
    #     Science — what's the smoothest reading path?"
    # ══════════════════════════════════════════════════════════════

    # Pre-defined genre proximity (lower = closer relationship)
    GENRE_DIST = {
        ('Fiction',         'Dystopia'):         1,
        ('Dystopia',        'Science Fiction'):  1,
        ('Fantasy',         'Science Fiction'):  1,
        ('Science Fiction', 'Computer Sci.'):    2,
        ('Self-Help',       'Psychology'):       1,
        ('Self-Help',       'Business'):         2,
        ('Finance',         'Business'):         1,
        ('History',         'Philosophy'):       2,
        ('Fiction',         'Romance'):          2,
        ('Philosophy',      'Self-Help'):        2,
    }

    def _heuristic(self, genre_a, genre_b):
        """A* heuristic: estimated genre-hop cost from genre_a to genre_b."""
        if genre_a == genre_b:
            return 0
        key = (genre_a, genre_b)
        rev = (genre_b, genre_a)
        return self.GENRE_DIST.get(key, self.GENRE_DIST.get(rev, 5))

    def astar_reading_path(self, start_id, goal_id):
        """
        A* search from start_id to goal_id through the book graph.
        Returns list of books forming the optimal path, or None if unreachable.
        """
        graph = self._get_graph()

        if start_id not in graph or goal_id not in graph:
            return None

        goal_genre = self._books_map[goal_id][3]
        h0         = self._heuristic(self._books_map[start_id][3], goal_genre)

        # heap entry: (f_cost, g_cost, node_id, path_so_far)
        heap   = [(h0, 0, start_id, [start_id])]
        best_g = {start_id: 0}

        while heap:
            f, g, node, path = heapq.heappop(heap)

            if node == goal_id:
                result = []
                for i, bid in enumerate(path):
                    b    = self._books_map[bid]
                    link = "Start"
                    if i > 0:
                        w    = graph[path[i-1]].get(bid, 99)
                        link = "Same Author" if w == 1 else "Same Genre"
                    result.append({
                        'step':   i + 1,
                        'id':     bid,
                        'title':  b[1],
                        'author': b[2],
                        'genre':  b[3],
                        'link':   link,
                    })
                return result

            for nbr, weight in graph[node].items():
                new_g = g + weight
                if nbr not in best_g or new_g < best_g[nbr]:
                    best_g[nbr] = new_g
                    h = self._heuristic(self._books_map[nbr][3], goal_genre)
                    heapq.heappush(heap, (new_g + h, new_g, nbr, path + [nbr]))

        return None  # No path exists

    # ══════════════════════════════════════════════════════════════
    #  1. FUZZY SEARCH (Levenshtein Edit Distance)
    # ══════════════════════════════════════════════════════════════

    def fuzzy_search(self, query):
        query = query.lower().strip()
        books = self.db.get_all_books()
        synonyms = {
            'sci-fi': 'science fiction', 'sf': 'science fiction',
            'scifi': 'science fiction',
            'cs': 'computer sci', 'programming': 'computer sci',
            'coding': 'computer sci',
            'money': 'finance', 'investment': 'finance',
            'story': 'fiction', 'novel': 'fiction',
            'self help': 'self-help', 'selfhelp': 'self-help',
        }
        expanded = synonyms.get(query, query)
        tokens   = set(re.split(r'\s+', expanded))
        results  = []

        for book in books:
            bid, title, author, genre = book[0], book[1], book[2], book[3]
            haystack = f"{title} {author} {genre}".lower()
            score    = 0
            if expanded in haystack:
                score = 100
            else:
                for token in tokens:
                    if len(token) < 2:
                        continue
                    if token in haystack:
                        score += 40
                    else:
                        for word in haystack.split():
                            ed  = self._edit_distance(token, word)
                            ml  = max(len(token), len(word))
                            if ml and (1 - ed/ml)*100 >= 70:
                                score = max(score, int((1-ed/ml)*80))
            if score >= 30:
                results.append({'id': bid, 'title': title, 'author': author,
                                'genre': genre, 'score': min(score, 100)})

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]

    def _edit_distance(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1
        dist = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            new = [i2 + 1]
            for i1, c1 in enumerate(s1):
                new.append(dist[i1] if c1 == c2 else 1 + min(dist[i1], dist[i1+1], new[-1]))
            dist = new
        return dist[-1]

    # ══════════════════════════════════════════════════════════════
    #  2. RECOMMENDATIONS (Collaborative Filtering)
    # ══════════════════════════════════════════════════════════════

    def recommend_books(self, member_id):
        history = self.db.get_member_borrow_history(member_id)
        if not history:
            return []
        borrowed_ids  = {r[0] for r in history}
        genre_counts  = {}
        for r in history:
            g = r[3] or 'General'
            genre_counts[g] = genre_counts.get(g, 0) + 1
        total         = sum(genre_counts.values())
        affinity      = {g: round(c/total*100) for g, c in genre_counts.items()}
        top_genre     = max(genre_counts, key=genre_counts.get)
        scored = []
        for b in self.db.get_all_books():
            if b[0] in borrowed_ids or b[6] <= 0:
                continue
            af = affinity.get(b[3], 0)
            if af > 0:
                reason = f"You often read {b[3]} books" if b[3] == top_genre else f"Matches your {b[3]} interest"
                scored.append({'id': b[0], 'title': b[1], 'author': b[2],
                               'genre': b[3], 'score': af, 'reason': reason})
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:5]

    # ══════════════════════════════════════════════════════════════
    #  3. INSIGHTS DASHBOARD
    # ══════════════════════════════════════════════════════════════

    def generate_insights(self):
        stats       = self.db.get_total_stats()
        genre_stats = self.db.get_genre_stats()
        top_books   = self.db.get_most_borrowed_books()
        overdue     = self.db.get_all_overdue()
        util        = round(stats['currently_issued'] / max(stats['total_books'],1) * 100, 1)

        L = []
        L.append("  ┌──────────────────────────────────────────────────┐")
        L.append("  │          📊  AI LIBRARY INSIGHTS                 │")
        L.append("  └──────────────────────────────────────────────────┘\n")
        L.append(f"  Total Books      : {stats['total_books']}")
        L.append(f"  Available        : {stats['available_books']}")
        L.append(f"  Currently Issued : {stats['currently_issued']}")
        L.append(f"  Total Members    : {stats['total_members']}")
        L.append(f"  Fines Collected  : ₹{stats['total_fines']:.2f}")
        L.append(f"  Utilization Rate : {util}%\n")
        L.append("  🤖 " + ("High utilization! Buy more copies." if util >= 60
                  else "Low utilization — run a member drive." if util <= 20
                  else "Utilization is healthy.") + "\n")

        if genre_stats:
            L.append("  📚 GENRE POPULARITY")
            L.append("  " + "─"*46)
            for g in genre_stats[:6]:
                L.append(f"  {g[0]:<18} {'█'*min(g[1]*3,20)} ({g[1]})")
            L.append(f"\n  🤖 Top genre: '{genre_stats[0][0]}'\n")

        if top_books:
            L.append("  🏆 MOST BORROWED BOOKS")
            L.append("  " + "─"*46)
            for i, b in enumerate(top_books, 1):
                L.append(f"  {i}. {b[0]} ({b[2]} borrows)")
            L.append("")

        if overdue:
            L.append(f"  ⚠️  {len(overdue)} OVERDUE BOOK(S)")
            for o in overdue[:3]:
                L.append(f"  • {o[2][:26]} — {o[1]} ({int(o[4])}d overdue)")
        else:
            L.append("  ✅ No overdue books!")

        return "\n".join(L)

    # ══════════════════════════════════════════════════════════════
    #  4. OVERDUE & FINE ANALYSIS
    # ══════════════════════════════════════════════════════════════

    def overdue_report(self):
        overdue = self.db.get_all_overdue()
        L = []
        L.append("  ┌──────────────────────────────────────────────────┐")
        L.append("  │       ⚠️  OVERDUE BOOKS & FINE ANALYSIS          │")
        L.append("  └──────────────────────────────────────────────────┘\n")

        if not overdue:
            L.append("  ✅ No overdue books found!")
            return "\n".join(L)

        total  = 0
        risks  = []
        L.append(f"  {'Member':<20} {'Title':<28} {'Due':<12} {'Days':<6} {'Fine':<8} Risk")
        L.append("  " + "─"*80)
        for o in overdue:
            days = int(o[4]); fine = days * 2.0; total += fine
            risk = "🔴 HIGH" if days > 30 else ("🟡 MED" if days > 14 else "🟢 LOW")
            risks.append((days, risk, o[1]))
            L.append(f"  {o[1]:<20} {o[2][:27]:<28} {o[3]:<12} {days:<6} ₹{fine:<7.2f} {risk}")
        L.append("  " + "─"*80)
        L.append(f"  Total fines: ₹{total:.2f}\n")
        L.append("  🤖 AI ANALYSIS")
        high = [r for r in risks if '🔴' in r[1]]
        if high:
            L.append(f"  • HIGH RISK: {', '.join(set(r[2] for r in high))}")
        avg = sum(r[0] for r in risks) / len(risks)
        L.append(f"  • Avg overdue: {avg:.1f} days")
        L.append(f"  • 💡 {'Send urgent notices!' if avg > 20 else 'Keep reminders going.'}")
        return "\n".join(L)
