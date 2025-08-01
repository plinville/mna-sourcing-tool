import sqlite3
import pandas as pd

class CandidateDatabase:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                website TEXT,
                summary TEXT,
                feedback TEXT,
                status TEXT
            )
            """
        )
        self.conn.commit()

    def insert_candidates(self, df):
        expected_columns = ["name", "website", "summary"]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = ""
        df_filtered = df[expected_columns].copy()
        df_filtered.to_sql("candidates", self.conn, if_exists="append", index=False)

    def get_unreviewed_candidates(self):
        query = "SELECT * FROM candidates WHERE feedback IS NULL"
        return pd.read_sql_query(query, self.conn)

    def update_feedback(self, candidate_id, feedback_text, status):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE candidates SET feedback = ?, status = ? WHERE id = ?",
            (feedback_text, status, candidate_id),
        )
        self.conn.commit()

    def get_approved_candidates(self):
        return pd.read_sql_query(
            "SELECT * FROM candidates WHERE status = 'approved'", self.conn
        )

    def get_all_candidates(self):
        return pd.read_sql_query("SELECT * FROM candidates", self.conn)
