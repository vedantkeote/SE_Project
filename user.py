class User:
    def __init__(self, user_id, name, email, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role  # student, staff, admin
        self.password = "password123"  # Simplified authentication for this demo

    def authenticate(self, user_id, password):
        return self.user_id == user_id and password == self.password

    def get_role(self):
        return self.role

    def get_name(self):
        return self.name
