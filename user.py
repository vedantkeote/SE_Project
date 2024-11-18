import json

class User:
    def __init__(self, user_id, name, email, role, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role  # 'student', 'staff', 'admin'
        self.password = password

    def authenticate(self, password):
        return self.password == password

    @staticmethod
    def register(user_id, name, email, role, password):
        new_user = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role,
            "password": password
        }
        with open('database.json', 'r+') as file:
            data = json.load(file)
            data['users'].append(new_user)
            file.seek(0)
            json.dump(data, file, indent=4)

        print("User registered successfully!")
