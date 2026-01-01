# storage/postgres.py
import psycopg2
from psycopg2.extras import RealDictCursor
import os

class PostgresStore:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            dbname=os.getenv("PG_DB", "researchai"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD", "postgres"),
            cursor_factory=RealDictCursor
        )

    def insert_paper(self, paper):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO papers (paper_id, title, year, venue, url, citations)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (paper_id) DO NOTHING
                """,
                (
                    paper.paper_id,
                    paper.title,
                    paper.year,
                    paper.venue,
                    paper.url,
                    paper.citations
                )
            )
            self.conn.commit()

    def fetch_papers_by_year(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM papers ORDER BY year")
            return cur.fetchall()
