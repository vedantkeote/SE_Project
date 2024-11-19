import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,
    QComboBox, QListWidget, QHBoxLayout
)

class OutpassManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
        self.setWindowTitle("Outpass Management System")
        self.setGeometry(100, 100, 500, 600)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        """Initialize the login interface."""
        self.clear_layout()  # Ensure the previous layout is cleared

        # UI for Login
        self.layout.addWidget(QLabel("User ID:"))
        self.user_id_input = QLineEdit()
        self.layout.addWidget(self.user_id_input)

        self.layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.show_registration)
        self.layout.addWidget(self.register_button)

        self.role_selector = QComboBox()
        self.role_selector.addItems(["student", "staff", "admin"])
        self.layout.addWidget(self.role_selector)

    def logout(self):
        """Logout the user and return to the login interface."""
        self.clear_layout()  # Ensure the previous layout is cleared
        self.initUI()

    def handle_login(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_selector.currentText().strip().lower()

        self.cursor.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
        user = self.cursor.fetchone()

        if user:
            db_role = user[4].strip().lower()
            if db_role == role:
                QMessageBox.information(self, "Login Success", f"Welcome {user[1]} ({role})!")
                self.show_dashboard(db_role, user)
            else:
                QMessageBox.warning(self, "Login Failed", f"Incorrect role selected. You are registered as '{db_role}'.")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid User ID or Password.")

    def show_registration(self):
        self.clear_layout()
        self.layout.addWidget(QLabel("Register New User"))

        self.register_user_id = QLineEdit(self)
        self.register_user_id.setPlaceholderText("User ID")
        self.layout.addWidget(self.register_user_id)

        self.register_name = QLineEdit(self)
        self.register_name.setPlaceholderText("Name")
        self.layout.addWidget(self.register_name)

        self.register_email = QLineEdit(self)
        self.register_email.setPlaceholderText("Email")
        self.layout.addWidget(self.register_email)

        self.register_password = QLineEdit(self)
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.setPlaceholderText("Password")
        self.layout.addWidget(self.register_password)

        self.register_role = QComboBox(self)
        self.register_role.addItems(["student", "staff", "admin"])
        self.layout.addWidget(self.register_role)

        register_button = QPushButton("Submit Registration", self)
        register_button.clicked.connect(self.register_user)
        self.layout.addWidget(register_button)

        back_button = QPushButton("Back to Login", self)
        back_button.clicked.connect(self.initUI)
        self.layout.addWidget(back_button)

    def register_user(self):
        user_id = self.register_user_id.text().strip()
        name = self.register_name.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text().strip()
        role = self.register_role.currentText().strip()

        self.cursor.execute("INSERT INTO users (user_id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
                            (user_id, name, email, password, role))
        self.conn.commit()
        QMessageBox.information(self, "Success", "User registered successfully!")
        self.initUI()

    def show_dashboard(self, role, user):
        self.clear_layout()
        if role == "student":
            self.show_student_dashboard(user)
        elif role == "staff":
            self.show_staff_dashboard()
        elif role == "admin":
            self.show_admin_dashboard()

        logout_button = QPushButton("Logout")
        logout_button.clicked.connect(self.initUI)
        self.layout.addWidget(logout_button)

    def load_notifications(self, student_id):
        """Load and display notifications for the student."""
        self.notifications_list.clear()  # Clear the current list

        # Fetch notifications from the database for the given student ID
        self.cursor.execute("SELECT message FROM notifications WHERE student_id=?", (student_id,))
        notifications = self.cursor.fetchall()

        if not notifications:
            self.notifications_list.addItem("No new notifications.")
        else:
            for notification in notifications:
                self.notifications_list.addItem(notification[0])

    def show_student_dashboard(self, user):
        self.layout.addWidget(QLabel(f"Welcome, {user[1]}"))
        self.layout.addWidget(QLabel("Notifications Panel"))
        self.notifications_list = QListWidget(self)
        self.layout.addWidget(self.notifications_list)
        self.load_notifications(user[0])

    def show_staff_dashboard(self):
        self.layout.addWidget(QLabel("Review Pending Outpasses"))
        self.outpass_list = QListWidget(self)
        self.layout.addWidget(self.outpass_list)
        self.load_pending_outpasses()

        approve_button = QPushButton("Approve")
        approve_button.clicked.connect(lambda: self.update_outpass_status("approved"))
        self.layout.addWidget(approve_button)

        reject_button = QPushButton("Reject")
        reject_button.clicked.connect(lambda: self.update_outpass_status("rejected"))
        self.layout.addWidget(reject_button)

    def show_admin_dashboard(self):
        self.layout.addWidget(QLabel("Admin Dashboard"))
        
        view_users_button = QPushButton("View All Users")
        view_users_button.clicked.connect(self.view_all_users)
        self.layout.addWidget(view_users_button)
        
        view_outpasses_button = QPushButton("View All Outpasses")
        view_outpasses_button.clicked.connect(self.view_all_outpasses)
        self.layout.addWidget(view_outpasses_button)

    def view_all_users(self):
        self.layout.addWidget(QLabel("All Registered Users"))
        users_list = QListWidget(self)
        self.layout.addWidget(users_list)
        self.cursor.execute("SELECT user_id, name, role FROM users")
        for user in self.cursor.fetchall():
            users_list.addItem(f"ID: {user[0]}, Name: {user[1]}, Role: {user[2]}")

    def view_all_outpasses(self):
        self.layout.addWidget(QLabel("All Outpasses"))
        outpasses_list = QListWidget(self)
        self.layout.addWidget(outpasses_list)
        self.cursor.execute("SELECT * FROM outpasses")
        for outpass in self.cursor.fetchall():
            outpasses_list.addItem(f"ID: {outpass[0]}, Student: {outpass[1]}, Status: {outpass[5]}")

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OutpassManagementSystem()
    window.show()
    sys.exit(app.exec())
