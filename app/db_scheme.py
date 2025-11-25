chats = """CREATE TABLE IF NOT EXISTS chats (
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_id INTEGER NOT NULL UNIQUE,
chat_title TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

users = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER NOT NULL,
username TEXT,
first_name TEXT,
last_name TEXT,
joined_at TEXT,
left_at TEXT,
is_member INTEGER
)
"""

events = """CREATE TABLE IF NOT EXISTS events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_id INTEGER NOT NULL,
chat_title TEXT NOT NULL,
user_id INTEGER NOT NULL,
username TEXT,
user_first_name TEXT,
user_last_name TEXT,
created_at TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users (id),
FOREIGN KEY (chat_id) REFERENCES chats (id)
)
"""