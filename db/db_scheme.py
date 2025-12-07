events = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_title TEXT NOT NULL,
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

users = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY NOT NULL UNIQUE ON CONFLICT IGNORE,
    username TEXT UNIQUE ON CONFLICT IGNORE,
    first_name TEXT,
    last_name TEXT,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


"""

chats = """
CREATE TABLE IF NOT EXISTS chats (
    chat_id BIGINT PRIMARY KEY NOT NULL UNIQUE ON CONFLICT IGNORE,
    chat_title TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

"""

is_member = """
CREATE TABLE IF NOT EXISTS is_member (
    user_id BIGINT NOT NULL REFERENCES users(user_id),
    chat_id BIGINT NOT NULL REFERENCES chats(chat_id),
    username TEXT,
    chat_title TEXT,
    PRIMARY KEY (user_id, chat_id)
);
"""
