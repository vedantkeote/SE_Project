import json

class Outpass:
    next_id = 1

    def __init__(self, student_id, date, time, reason):
        self.outpass_id = Outpass.next_id
        Outpass.next_id += 1
        self.student_id = student_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = "pending"

    def save_outpass(self):
        new_outpass = {
            "outpass_id": self.outpass_id,
            "student_id": self.student_id,
            "date": self.date,
            "time": self.time,
            "reason": self.reason,
            "status": self.status
        }
        with open('database.json', 'r+') as file:
            data = json.load(file)
            data['outpasses'].append(new_outpass)
            file.seek(0)
            json.dump(data, file, indent=4)
