import json
import os

class Storage:
    def __init__(self, file):
        self.file = file

    def load(self):
        if not os.path.exists(self.file):
            return {"high_score": 0}
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f)