class Notification:
    def __init__(self, message, recipient_id):
        self.message = message
        self.recipient_id = recipient_id

    def display(self):
        print(f"Notification for {self.recipient_id}: {self.message}")
