from user import User
from outpass import Outpass
from notification import Notification

# Sample Data
users = [
    User("1", "Alice", "alice@example.com", "student"),
    User("2", "Bob", "bob@example.com", "staff"),
    User("3", "Charlie", "charlie@example.com", "admin")
]

outpasses = []
notifications = []

# User Login
def login():
    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    for user in users:
        if user.authenticate(user_id, password):
            print(f"Login successful! Welcome {user.get_name()}")
            if user.get_role() == "student":
                student_menu(user)
            elif user.get_role() == "staff":
                staff_menu(user)
            elif user.get_role() == "admin":
                admin_menu()
            return

    print("Invalid credentials. Try again.")
    login()

# Student Menu
def student_menu(user):
    while True:
        print("\n1. Apply for Outpass\n2. View Notifications\n3. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            apply_outpass(user)
        elif choice == "2":
            view_notifications(user)
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

# Apply for Outpass
def apply_outpass(user):
    date = input("Enter Date (YYYY-MM-DD): ")
    time = input("Enter Time (HH:MM): ")
    reason = input("Enter Reason: ")

    outpass = Outpass(user.get_name(), date, time, reason)
    outpasses.append(outpass)
    print("Outpass request submitted.")

# Staff Menu
def staff_menu(user):
    while True:
        print("\n1. Approve/Reject Outpasses\n2. Logout")
        choice = input("Choose an option: ")

        if choice == "1":
            approve_reject_outpass()
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

# Approve/Reject Outpasses
def approve_reject_outpass():
    for outpass in outpasses:
        if outpass.status == "pending":
            outpass.display()
            decision = input("Approve (yes/no)? ")
            status = "approved" if decision.lower() == "yes" else "rejected"
            outpass.update_status(status)
            notifications.append(Notification(f"Your outpass has been {status}", outpass.student_id))
            print(f"Outpass {outpass.outpass_id} has been {status}.")

# Admin Menu
def admin_menu():
    generate_reports()

# Generate Reports
def generate_reports():
    print("\nOutpass Report:")
    for outpass in outpasses:
        outpass.display()

# View Notifications
def view_notifications(user):
    print("\nNotifications:")
    for notification in notifications:
        if notification.recipient_id == user.get_name():
            notification.display()

# Main Function
if __name__ == "__main__":
    print("Welcome to the Outpass Management System!")
    login()
