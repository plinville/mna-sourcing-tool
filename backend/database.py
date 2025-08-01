import sqlite3

class CandidateDatabase:
    def __init__(self, db_path="candidates.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                description TEXT,
                feedback TEXT
            )
        """)
        self.conn.commit()

    def get_unreviewed_candidates(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, website, description FROM candidates WHERE feedback IS NULL")
        return cursor.fetchall()

    def update_feedback(self, candidate_id, feedback):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE candidates SET feedback = ? WHERE id = ?", (feedback, candidate_id))
        self.conn.commit()

    def add_candidate(self, name, website, description):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO candidates (name, website, description) VALUES (?, ?, ?)", (name, website, description))
        self.conn.commit()
