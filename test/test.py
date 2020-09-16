from ctypes import c_uint64, c_uint8, Structure, Union

spec = {
    "opcode": 3,
    "pop_push": 1,
    "memory_type": 2,
    "sram_addr": 16,
    "dram_addr": 32,
    "size": 16,
    "stride": 16,
    "pad": 4,
}


InstrBytes = c_uint8 * 16


class InstrBits(Structure):
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint64, spec["opcode"]),
        ("pop_prev_dep", c_uint64, spec["pop_push"]),
        ("pop_next_dep", c_uint64, spec["pop_push"]),
        ("push_prev_dep", c_uint64, spec["pop_push"]),
        ("push_next_dep", c_uint64, spec["pop_push"]),
        ("memory_type", c_uint64, spec["memory_type"]),
        ("sram_base", c_uint64, spec["sram_addr"]),
        ("dram_base", c_uint64, spec["dram_addr"]),
        ("y_size", c_uint64, spec["size"]),
        ("x_size", c_uint64, spec["size"]),
        ("x_stride", c_uint64, spec["stride"]),
        ("y_pad_0", c_uint64, spec["pad"]),
        ("y_pad_1", c_uint64, spec["pad"]),
        ("x_pad_0", c_uint64, spec["pad"]),
        ("x_pad_1", c_uint64, spec["pad"]),
    ]


class Instr(Union):
    _fields_ = [("field", InstrBits), ("asbyte", InstrBytes)]

    def __str__(self):
        x = list(bytes(self.asbyte))
        x.reverse()
        y = ["{:02x}".format(i) for i in x]
        return "".join(y)


instr = Instr()
instr.field.opcode = 0
instr.field.memory_type = 3
instr.field.dram_base = 0x82
instr.field.y_size = 1
instr.field.x_size = 1

print(instr)

# from collections import OrderedDict

# class Field(object):
#     def __init__(self, value, width):
#         self.value = value
#         self.width = width

#     def __str__(self):
#         return "{}".format(self.value)

#     def get_width(self):
#         return self.width

#     def get_value(self):
#         return self.value

# class Instr(object):
#     def __init__(self, width):
#         self.width = width
#         self.layout = OrderedDict()

#     def set_field(self, index, field):
#         self.layout[index] = field

#     def get_field(self, index):
#         return self.layout[index]

#     def debug(self):
#         for k, v in self.layout.items():
#             print("{} {}".format(k, v))


# instr = Instr(128)
# instr.set_field(0, Field(0, 3))
# instr.set_field(1, Field(0, 1))
# instr.set_field(2, Field(0, 1))
# instr.set_field(3, Field(0, 1))
# instr.set_field(4, Field(0, 1))
# instr.set_field(5, Field(3, 2))


# instr.debug()
