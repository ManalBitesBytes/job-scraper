import csv

class CSVLoader():
    def __init__(self, filename):
        self.filename = filename

    def load(self, data):
        keys = data[0].keys() if data else []
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


