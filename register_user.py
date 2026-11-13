import sqlite3
import hashlib

def validate_password(password):
    if len(password) < 8:
        return False
    has_number = False
    for char in password:
        if char.isdigit():
            has_number = True
            break
    return has_number

def register():
    username = input("Enter a new username: ")
    password = input("Enter a secure password: ")
    
    if not validate_password(password):
        print("Registration failed: Password must be 8+ characters and contain a number.")
        return

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect('auth_system.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO Users (username, password_hash) 
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        print(f"Success! Account for '{username}' created securely.")
    except sqlite3.IntegrityError:
        print(f"Error: The username '{username}' is already taken.")
    finally:
        conn.close()

if __name__ == "__main__":
    register()
