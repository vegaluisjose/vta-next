from collections import OrderedDict

class Field(object):
    def __init__(self, value, width):
        self.value = value
        self.width = width

    def __str__(self):
        return "{}".format(self.value)

    def get_width(self):
        return self.width

    def get_value(self):
        return self.value

class Instr(object):
    def __init__(self, width):
        self.width = width
        self.layout = OrderedDict()

    def set_field(self, index, field):
        self.layout[index] = field

    def get_field(self, index):
        return self.layout[index]

    def debug(self):
        for k, v in self.layout.items():
            print("{} {}".format(k, v))


instr = Instr(128)
instr.set_field(0, Field(0, 3))
instr.set_field(1, Field(0, 1))
instr.set_field(2, Field(0, 1))
instr.set_field(3, Field(0, 1))
instr.set_field(4, Field(0, 1))
instr.set_field(5, Field(3, 2))


instr.debug()