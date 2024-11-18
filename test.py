import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT,
            role TEXT
        )
    ''')
    
    # Create Outpasses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS outpasses (
            outpass_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            FOREIGN KEY(student_id) REFERENCES users(user_id)
        )
    ''')
    
    # Insert Dummy Users
    dummy_users = [
        ("s001", "Alice", "alice@student.com", "password123", "student"),
        ("s002", "Bob", "bob@student.com", "password123", "student"),
        ("staff001", "Charlie", "charlie@staff.com", "password123", "staff"),
        ("admin001", "David", "david@admin.com", "password123", "admin")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (user_id, name, email, password, role)
        VALUES (?, ?, ?, ?, ?)
    ''', dummy_users)

    conn.commit()
    conn.close()

    print("Database initialized with dummy users.")

if __name__ == "__main__":
    init_db()
