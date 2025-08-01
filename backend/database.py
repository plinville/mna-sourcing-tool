import sqlite3
import pandas as pd

class CandidateDatabase:
    def __init__(self, db_path="candidates.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                summary TEXT,
                feedback TEXT
            )
            """
        )

    def insert_candidates(self, df):
        if df.empty:
            return
        df.to_sql("candidates", self.conn, if_exists="append", index=False)

    def get_unreviewed_candidates(self, limit=1):
        query = "SELECT * FROM candidates WHERE feedback IS NULL LIMIT ?"
        return pd.read_sql_query(query, self.conn, params=(limit,))

    def update_feedback(self, candidate_id, feedback):
        self.conn.execute(
            "UPDATE candidates SET feedback = ? WHERE id = ?", (feedback, candidate_id)
        )
        self.conn.commit()
