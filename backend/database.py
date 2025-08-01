import sqlite3
import pandas as pd

class CandidateDatabase:
    def __init__(self, db_path="candidates_v2.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

        # 🛠️ Add 'status' column if missing
        try:
            self.conn.execute("ALTER TABLE candidates ADD COLUMN status TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                summary TEXT,
                feedback TEXT,
                status TEXT
            )
            """)

    def insert_candidates(self, df):
        expected_columns = ["name", "website", "summary"]
        df_filtered = df[expected_columns].copy()
        df_filtered["feedback"] = None
        df_filtered["status"] = None
        df_filtered.to_sql("candidates", self.conn, if_exists="append", index=False)

    def get_unreviewed_candidates(self):
        query = "SELECT * FROM candidates WHERE feedback IS NULL"
        return pd.read_sql_query(query, self.conn)

    def update_feedback(self, candidate_id, feedback, status):
        with self.conn:
            self.conn.execute(
                "UPDATE candidates SET feedback = ?, status = ? WHERE id = ?",
                (feedback, status, candidate_id)
            )

    def get_approved_candidates(self):
        return pd.read_sql_query(
            "SELECT * FROM candidates WHERE status = 'approved'", self.conn
        )

    def get_all_candidates(self):
        return pd.read_sql_query("SELECT * FROM candidates", self.conn)
