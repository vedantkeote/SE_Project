import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QComboBox, QListWidget
)

class OutpassManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        
        self.setWindowTitle("Outpass Management System")
        self.setGeometry(100, 100, 400, 500)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
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

    def handle_login(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()
        role = self.role_selector.currentText()

        self.cursor.execute("SELECT * FROM users WHERE user_id=? AND password=? AND role=?", (user_id, password, role))
        user = self.cursor.fetchone()

        if user:
            QMessageBox.information(self, "Login Success", f"Welcome {user[1]}!")
            self.show_dashboard(role, user)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

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
        user_id = self.register_user_id.text()
        name = self.register_name.text()
        email = self.register_email.text()
        password = self.register_password.text()
        role = self.register_role.currentText()

        if not user_id or not name or not email or not password:
            QMessageBox.warning(self, "Registration Error", "All fields are required.")
            return

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
            QMessageBox.information(self, "Admin", "Admin Dashboard coming soon!")

    def show_student_dashboard(self, user):
        self.layout.addWidget(QLabel(f"Welcome, {user[1]}"))
        self.date_input = QLineEdit(self)
        self.date_input.setPlaceholderText("Date (YYYY-MM-DD)")
        self.layout.addWidget(self.date_input)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Time (HH:MM)")
        self.layout.addWidget(self.time_input)

        self.reason_input = QLineEdit(self)
        self.reason_input.setPlaceholderText("Reason")
        self.layout.addWidget(self.reason_input)

        submit_button = QPushButton("Submit Outpass Request")
        submit_button.clicked.connect(lambda: self.submit_outpass_request(user[0]))
        self.layout.addWidget(submit_button)

    def show_staff_dashboard(self):
        self.layout.addWidget(QLabel("Review Outpasses"))
        self.outpass_list = QListWidget(self)
        self.layout.addWidget(self.outpass_list)

        self.cursor.execute("SELECT * FROM outpasses WHERE status='pending'")
        for row in self.cursor.fetchall():
            self.outpass_list.addItem(f"ID: {row[0]}, Student: {row[1]}, Date: {row[2]}, Reason: {row[4]}")

    def submit_outpass_request(self, student_id):
        date = self.date_input.text()
        time = self.time_input.text()
        reason = self.reason_input.text()
        self.cursor.execute("INSERT INTO outpasses (student_id, date, time, reason) VALUES (?, ?, ?, ?)",
                            (student_id, date, time, reason))
        self.conn.commit()
        QMessageBox.information(self, "Success", "Outpass request submitted.")

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
