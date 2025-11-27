events = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    chat_id INTEGER NOT NULL,
    chat_title TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    username TEXT,
    user_first_name TEXT,
    user_last_name TEXT,
    created_at TEXT NOT NULL
);
"""

users = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    user_first_name TEXT,
    user_last_name TEXT,
    created_at TEXT,
    left_at TEXT,
    last_activity TEXT,
    is_member INTEGER
);
"""
