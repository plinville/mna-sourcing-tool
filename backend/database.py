import sqlite3
import pandas as pd
import os

class CandidateDatabase:
    def __init__(self, db_path="candidates.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
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
        if df.empty:
            return
        expected_columns = ["name", "website", "summary"]
        df_filtered = df[expected_columns].copy()
        df_filtered["feedback"] = None
        df_filtered.to_sql("candidates", self.conn, if_exists="append", index=False)

    def get_unreviewed_candidates(self):
        query = "SELECT * FROM candidates WHERE feedback IS NULL"
        return pd.read_sql_query(query, self.conn)

    def update_feedback(self, candidate_id, feedback):
        query = "UPDATE candidates SET feedback = ? WHERE id = ?"
        self.conn.execute(query, (feedback, candidate_id))
        self.conn.commit()
