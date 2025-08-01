import sqlite3
from datetime import datetime

class CandidateDatabase:
    def __init__(self, db_file="candidates.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                description TEXT,
                date_added TEXT,
                feedback TEXT
            )
        """)
        self.conn.commit()

    def add_candidate(self, name, website, description):
        now = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT INTO candidates (name, website, description, date_added) VALUES (?, ?, ?, ?)",
            (name, website, description, now),
        )
        self.conn.commit()

    def get_unreviewed(self, limit=1):
        cursor = self.conn.execute(
            "SELECT id, name, website, description FROM candidates WHERE feedback IS NULL LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()

    def submit_feedback(self, candidate_id, feedback):
        self.conn.execute(
            "UPDATE candidates SET feedback = ? WHERE id = ?",
            (feedback, candidate_id)
        )
        self.conn.commit()
