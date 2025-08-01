import sqlite3
import pandas as pd

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
                summary TEXT,
                feedback TEXT
            )
        """)
        self.conn.commit()

    def insert_candidates(self, df):
        # Ensure required columns exist
        expected_columns = ["name", "website", "summary"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        df_filtered = df[expected_columns].copy()
        df_filtered["feedback"] = None  # Add empty feedback column
        df_filtered.drop_duplicates(subset=["website"], inplace=True)
        df_filtered.to_sql("candidates", self.conn, if_exists="append", index=False)

    def get_unreviewed_candidates(self):
        query = "SELECT * FROM candidates WHERE feedback IS NULL OR feedback = '' OR TRIM(feedback) = '' LIMIT 1"
        return pd.read_sql_query(query, self.conn)

    def update_feedback(self, candidate_id, feedback):
        # Ensure candidate_id is a native Python int
        candidate_id = int(candidate_id)
        self.conn.execute(
            "UPDATE candidates SET feedback = ? WHERE id = ?",
            (feedback, candidate_id)
        )
        self.conn.commit()
