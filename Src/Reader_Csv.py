import csv

class Reader_Csv:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                