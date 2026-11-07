import sqlite3

conn = sqlite3.connect('auth_system.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    is_locked INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Threat_Logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully!")