import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "runs.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    api TEXT,
    summary TEXT,
    tests TEXT
)
"""

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def save_run(run):
    conn = get_conn()
    conn.execute(CREATE_TABLE)
    conn.execute(
        "INSERT INTO runs (timestamp, api, summary, tests) VALUES (?, ?, ?, ?)",
        (run["timestamp"], run["api"], json.dumps(run["summary"]), json.dumps(run["tests"]))
    )
    conn.commit()
    conn.close()

def list_runs(limit=50):
    conn = get_conn()
    conn.execute(CREATE_TABLE)
    cur = conn.execute("SELECT timestamp, api, summary, tests FROM runs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "timestamp": r[0],
            "api": r[1],
            "summary": json.loads(r[2]),
            "tests": json.loads(r[3])
        }
        for r in rows
    ]
