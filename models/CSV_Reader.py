from models.Packages import Packages
from models.Distances import address_table
from models.Distances import find_shortest_distance
from models.Distances import distance_home
import datetime


def reset():
    Delivery.package_list.add("9", ['9', '300 State St', 'Salt Lake City', 'UT', '84103', 'EOD', '2',
                                    'Wrong address listed'])


class Delivery:
    package_list = Packages().hash_table
    speed = 18 / 60

    def __init__(self):
        reset()

        # truck 1
        self.truck1_distance = 0.0
        self.truck1_packages = [13, 14, 15, 16, 29, 30, 31, 34, 37, 40, 1, 4, 7, 39, 8, 32]
        self.truck1_priority = [13, 14, 15, 16, 29, 30, 31, 34, 37, 40]
        self.truck1_destinations = []
        self.truck1_destinations_priority = []
        self.truck1_position = 0
        self.truck1_position_current = 0.0
        self.truck1_goal = 0.0
        self.truck1_returned = False
        self.truck1_departed = False

        # truck 2
        self.truck2_distance = 0.0
        self.truck2_packages = [3, 18, 36, 38, 6, 10, 11, 12, 17, 20, 21, 22, 23, 24, 25, 26]
        self.truck2_priority = [6, 20, 25]
        self.truck2_destinations = []
        self.truck2_destinations_priority = []
        self.truck2_position = 0
        self.truck2_position_current = 0.0
        self.truck2_goal = 0.0
        self.truck2_returned = False
        self.truck2_departed = False

        # truck 3
        self.truck3_distance = 0.0
        self.truck3_packages = [9, 19, 27, 28, 33, 35, 2, 5]
        self.truck3_priority = []
        self.truck3_destinations = []
        self.truck3_destinations_priority = []
        self.truck3_position = 0
        self.truck3_position_current = 0.0
        self.truck3_goal = 0.0
        self.truck3_returned = False
        self.truck3_departed = False

        self.package_deliveries = [None] * 41

    # gets total distance traveled
    def total_distance(self):
        return float(self.truck1_distance + self.truck2_distance + self.truck3_distance)

    # builds lists depending on packages
    # space-time complexity is O(N)
    def __build_lists(self):
        for index in self.truck1_packages:
            address = Delivery.package_list.get(str(index))[1]
            address_id = address_table.get(address)[0]

            if address_id not in self.truck1_destinations:
                self.truck1_destinations.append(address_id)
                if index in self.truck1_priority:
                    self.truck1_destinations_priority.append(address_id)

        for index in self.truck2_packages:
            address = Delivery.package_list.get(str(index))[1]
            address_id = address_table.get(address)[0]

            if address_id not in self.truck2_destinations:
                self.truck2_destinations.append(address_id)
                if index in self.truck2_priority:
                    self.truck2_destinations_priority.append(address_id)

        for index in self.truck3_packages:
            address = Delivery.package_list.get(str(index))[1]
            address_id = address_table.get(address)[0]

            if address_id not in self.truck3_destinations:
                self.truck3_destinations.append(address_id)
                if index in self.truck3_priority:
                    self.truck3_destinations_priority.append(address_id)

    # unloads packages from lists once they are delivered
    # space-time complexity is O(N)
    def __unload_packages(self, truck_list, priority_list, location):
        self.removal_list = []
        for index in truck_list:
            address = Delivery.package_list.get(str(index))[1]
            address_id = address_table.get(address)[0]

            if address_id == str(location):
                self.removal_list.append(index)
                self.package_deliveries[index] = self.current_time.time()

        for item in self.removal_list:
            truck_list.remove(item)
            if item in priority_list:
                priority_list.remove(item)

    # method to perform package delivery
    # space-time complexity worse-case is O(inf)
    def run(self, time):
        self.sim_end = datetime.datetime.strptime(time, '%H:%M').time()
        self.current_time = datetime.datetime.strptime('08:00', '%H:%M')
        self.__build_lists()

        # sets destination for all trucks, chooses priority packages first
        if len(self.truck1_destinations_priority) > 0:
            self.truck1_next = find_shortest_distance(self.truck1_position, self.truck1_destinations_priority)
        elif len(self.truck1_destinations) > 0:
            self.truck1_next = find_shortest_distance(self.truck1_position, self.truck1_destinations)
        self.truck1_goal = float(self.truck1_next[1])

        if len(self.truck2_destinations_priority) > 0:
            self.truck2_next = find_shortest_distance(self.truck2_position, self.truck2_destinations_priority)
        elif len(self.truck2_destinations) > 0:
            self.truck2_next = find_shortest_distance(self.truck2_position, self.truck2_destinations)
        self.truck2_goal = float(self.truck2_next[1])

        if len(self.truck3_destinations_priority) > 0:
            self.truck3_next = find_shortest_distance(self.truck3_position, self.truck3_destinations_priority)
        elif len(self.truck3_destinations) > 0:
            self.truck3_next = find_shortest_distance(self.truck3_position, self.truck3_destinations)
        self.truck3_goal = float(self.truck3_next[1])

        self.truck1_departed = True

        # continues to run until all packages are unloaded or end destination is reached
        while not ((len(self.truck1_destinations) < 1 and len(self.truck2_destinations) < 1 and len(
                self.truck3_destinations) < 1) or (self.current_time.time() >= self.sim_end)):

            self.current_time += datetime.timedelta(minutes=1)

            # triggers truck 2 and truck 3 to depart
            if self.current_time.time() == datetime.datetime.strptime('09:05:00', '%H:%M:%S').time():
                self.truck2_departed = True
            if self.truck1_returned and self.current_time.time() >= datetime.datetime.strptime('10:20:00',
                                                                                               '%H:%M:%S').time():
                Delivery.package_list.add("9", ["9", "410 S State St", "Salt Lake City", "UT", "84111", "EOD", "2",
                                                "None"])
                self.truck3_departed = True

            if not self.truck1_returned and self.truck1_departed:
                self.truck1_position_current += Delivery.speed
                self.truck1_distance += Delivery.speed
            if not self.truck2_returned and self.truck2_departed:
                self.truck2_position_current += Delivery.speed
                self.truck2_distance += Delivery.speed
            if not self.truck3_returned and self.truck3_departed:
                self.truck3_position_current += Delivery.speed
                self.truck3_distance += Delivery.speed

            # truck 1 - delivers all packages then returns to hub
            if self.truck1_position_current >= self.truck1_goal:
                self.truck1_position_current -= self.truck1_goal
                self.truck1_position = self.truck1_next[0]
                self.__unload_packages(self.truck1_packages, self.truck1_priority, self.truck1_position)
                self.truck1_destinations.remove(self.truck1_next[0])
                # finds closest destination
                if len(self.truck1_destinations_priority) > 0:
                    self.truck1_destinations_priority.remove(self.truck1_next[0])
                if len(self.truck1_destinations_priority) > 0:
                    self.truck1_next = find_shortest_distance(self.truck1_position, self.truck1_destinations_priority)
                elif len(self.truck1_destinations) > 0:
                    self.truck1_next = find_shortest_distance(self.truck1_position, self.truck1_destinations)
                elif len(self.truck1_destinations) < 1 and self.truck1_next[0] != 0:
                    self.truck1_destinations.append(0)
                    self.truck1_next = (0, distance_home(self.truck1_position))
                self.truck1_goal = float(self.truck1_next[1])

            # truck 2 - delivers all packages then returns to hub
            if self.truck2_position_current >= self.truck2_goal:
                self.truck2_position_current -= self.truck2_goal
                self.truck2_position = self.truck2_next[0]
                self.__unload_packages(self.truck2_packages, self.truck2_priority, self.truck2_position)
                self.truck2_destinations.remove(self.truck2_next[0])
                # finds closest destination
                if len(self.truck2_destinations_priority) > 0:
                    self.truck2_destinations_priority.remove(self.truck2_next[0])
                if len(self.truck2_destinations_priority) > 0:
                    self.truck2_next = find_shortest_distance(self.truck2_position, self.truck2_destinations_priority)
                elif len(self.truck2_destinations) > 0:
                    self.truck2_next = find_shortest_distance(self.truck2_position, self.truck2_destinations)
                elif len(self.truck2_destinations) < 1 and self.truck2_next[0] != 0:
                    self.truck2_destinations.append(0)
                    self.truck2_next = (0, distance_home(self.truck2_position))
                self.truck2_goal = float(self.truck2_next[1])

            # truck 3 - delivers all packages then returns to hub
            if self.truck3_position_current >= self.truck3_goal:
                self.truck3_position_current -= self.truck3_goal
                self.truck3_position = self.truck3_next[0]
                self.__unload_packages(self.truck3_packages, self.truck3_priority, self.truck3_position)
                self.truck3_destinations.remove(self.truck3_next[0])
                # finds closest destination
                if len(self.truck3_destinations_priority) > 0:
                    self.truck3_destinations_priority.remove(self.truck3_next[0])
                if len(self.truck3_destinations_priority) > 0:
                    self.truck3_next = find_shortest_distance(self.truck3_position, self.truck3_destinations_priority)
                elif len(self.truck3_destinations) > 0:
                    self.truck3_next = find_shortest_distance(self.truck3_position, self.truck3_destinations)
                elif len(self.truck3_destinations) < 1 and self.truck3_next[0] != 0:
                    self.truck3_destinations.append(0)
                    self.truck3_next = (0, distance_home(self.truck3_position))
                self.truck3_goal = float(self.truck3_next[1])
            # stops adding mileage once truck is returned to hub
            if len(self.truck1_destinations) < 1:
                self.truck1_returned = True
            if len(self.truck2_destinations) < 1:
                self.truck2_returned = True
            if len(self.truck3_destinations) < 1:
                self.truck3_returned = True

    # used to receive input in the CLI
    def print(self, package_id=None):
        if package_id is None:
            for index in range(1, 41):
                self.package = Delivery.package_list.get(str(index))

                if self.package_deliveries[index] is not None:
                    self.package.append(str(self.package_deliveries[index]))
                elif (int(index) in self.truck1_packages and self.truck1_departed) or (
                        int(index) in self.truck2_packages and self.truck2_departed) or (
                        int(index) in self.truck3_packages and self.truck3_departed):
                    self.package.append("Out for Delivery")
                else:
                    self.package.append("At Hub")
                print(self.package)
                self.package.pop()
        else:
            self.package = Delivery.package_list.get(str(package_id))
            if self.package_deliveries[package_id] is not None:
                self.package.append(str(self.package_deliveries[package_id]))
            elif (int(package_id) in self.truck1_packages and self.truck1_departed) or (
                    int(package_id) in self.truck2_packages and self.truck2_departed) or (
                    int(package_id) in self.truck3_packages and self.truck3_departed):
                self.package.append("Out for Delivery")
            else:
                self.package.append("At Hub")
            print(self.package)
            self.package.pop()
        return

    def reset(self):
        pass
