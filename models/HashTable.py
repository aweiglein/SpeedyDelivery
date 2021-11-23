class HashTable:
    def __init__(self, size=16):
        self.map = [None] * size

    def __get_hash(self, key):
        if isinstance(key, int):
            return int(key) % len(self.map)
        else:
            return ord(key[0]) % len(self.map)

    def add(self, key, value):
        key_hash = self.__get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for item in self.map[key_hash]:
                if item[0] == key:
                    item[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        for item in self.map[self.__get_hash(key)]:
            if item[0] == key:
                return item[1]
        return None

    def delete(self, key):
        key_hash = self.__get_hash(key)
        index = 0

        for item in self.map[key_hash]:
            if item[0] == key:
                self.map[key_hash].pop(index)
                return True
            index += 1
        return False
