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

    # Create Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            message TEXT,
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

    # Insert Dummy Outpasses
    dummy_outpasses = [
        (None, "s001", "2024-11-20", "10:00", "Family Visit", "pending"),
        (None, "s002", "2024-11-21", "14:00", "Medical Appointment", "approved"),
        (None, "s001", "2024-11-22", "16:00", "Event Participation", "rejected")
    ]
    
    cursor.executemany('''
        INSERT INTO outpasses (outpass_id, student_id, date, time, reason, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', dummy_outpasses)

    # Insert Dummy Notifications
    dummy_notifications = [
        (None, "s001", "Your outpass request (ID: 2) has been approved."),
        (None, "s001", "Your outpass request (ID: 3) has been rejected."),
        (None, "s002", "Your outpass request (ID: 1) is still pending review.")
    ]
    
    cursor.executemany('''
        INSERT INTO notifications (notification_id, student_id, message)
        VALUES (?, ?, ?)
    ''', dummy_notifications)

    conn.commit()
    conn.close()
    print("Database initialized with dummy data.")

if __name__ == "__main__":
    init_db()
