import csv
from .HashTable import HashTable


class Packages:
    hash_table = HashTable()

    def __init__(self):
        with open('data/package_data.csv') as file:
            self.data = csv.reader(file, delimiter=',')
            for line in self.data:
                self.key = line[0]
                Packages.hash_table.add(self.key, [self.key, line[1], line[2], line[3], line[4], line[5], line[6], line[7]])
