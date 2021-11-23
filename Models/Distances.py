import csv
from Models.HashTable import HashTable

distance_data = list(csv.reader(open('Data/distance_data.csv'), delimiter=','))
address_data = list(csv.reader(open('Data/address_data.csv'), delimiter=','))
address_table = HashTable()

with open('Data/address_data.csv') as file:
    address = csv.reader(file, delimiter=",")
    for line in address:
        key = line[2]
        address_table.add(key, [line[0], line[1], key])


def find_shortest_distance(start, destinations):
    start = int(start)
    closest_distance = 100.0
    closest_location = None
    for distance in [less for less in destinations if int(less) < start]:
        if float(distance_data[start][int(distance)]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[start][int(distance)]
    for distance in [greater for greater in destinations if int(greater) > start]:
        if float(distance_data[int(distance)][start]) < float(closest_distance) and distance in destinations:
            closest_location = distance
            closest_distance = distance_data[int(distance)][start]
    return closest_location, closest_distance


def distance_home(start):
    return float(distance_data[int(start)][0])
