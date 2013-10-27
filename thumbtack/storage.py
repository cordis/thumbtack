from collections import defaultdict


class Storage(object):
    def __init__(self):
        self.name_to_value_map = {}
        self.value_counter_map = defaultdict(int)

    def set(self, name, value):
        self.delete(name)
        self.name_to_value_map[name] = value
        self.value_counter_map[value] += 1

    def get(self, name):
        return self.name_to_value_map.get(name)

    def delete(self, name):
        try:
            value = self.name_to_value_map.pop(name)
        except KeyError:
            pass
        else:
            self.value_counter_map[value] -= 1

    def get_count_equal_to(self, value):
        return self.value_counter_map.get(value, 0)
