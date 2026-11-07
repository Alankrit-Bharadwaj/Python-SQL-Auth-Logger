import sqlite3
import hashlib

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    attempted_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('auth_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password_hash, failed_attempts, is_locked FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user is None:
        print("Error: Username not found.")
        conn.close()
        return

    stored_hash = user[0]
    failed_attempts = user[1]
    is_locked = user[2]

    if is_locked == 1:
        print("SECURITY ALERT: Account is locked due to multiple failed attempts. Contact IT support.")
        conn.close()
        return

    if attempted_hash == stored_hash:
        print("Login successful! Access granted.")
        cursor.execute("UPDATE Users SET failed_attempts = 0 WHERE username = ?", (username,))
        cursor.execute("INSERT INTO Threat_Logs (username, event_type) VALUES (?, ?)", (username, "Successful Login"))
    else:
        new_fails = failed_attempts + 1
        
        if new_fails >= 3:
            cursor.execute("UPDATE Users SET failed_attempts = ?, is_locked = 1 WHERE username = ?", (new_fails, username))
            cursor.execute("INSERT INTO Threat_Logs (username, event_type) VALUES (?, ?)", (username, "ACCOUNT LOCKED - Suspected Brute Force"))
            print(f"Incorrect password. Attempt {new_fails} of 3.")
            print("SECURITY ALERT: Maximum attempts reached. Account locked.")
        else:
            cursor.execute("UPDATE Users SET failed_attempts = ? WHERE username = ?", (new_fails, username))
            cursor.execute("INSERT INTO Threat_Logs (username, event_type) VALUES (?, ?)", (username, "Failed Login Attempt"))
            print(f"Incorrect password. Attempt {new_fails} of 3.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    login()