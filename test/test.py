from ctypes import c_uint64, c_uint8, LittleEndianStructure, Union

SPEC_WIDTH = {
    "opcode": 3,
    "pop_push": 1,
    "memory_type": 2,
    "sram_addr": 16,
    "dram_addr": 32,
    "size": 16,
    "stride": 16,
    "pad": 4,
}

class InstrBits(LittleEndianStructure):
    _fields_ = [
        ("opcode", c_uint64, SPEC_WIDTH["opcode"]),
        ("pop_prev_dep", c_uint64, SPEC_WIDTH["pop_push"]),
        ("pop_next_dep", c_uint64, SPEC_WIDTH["pop_push"]),
        ("push_prev_dep", c_uint64, SPEC_WIDTH["pop_push"]),
        ("push_next_dep", c_uint64, SPEC_WIDTH["pop_push"]),
        ("memory_type", c_uint64, SPEC_WIDTH["memory_type"]),
        ("sram_base", c_uint64, SPEC_WIDTH["sram_addr"]),
        ("dram_base", c_uint64, SPEC_WIDTH["dram_addr"]),
        ("y_size", c_uint64, SPEC_WIDTH["size"]),
        ("x_size", c_uint64, SPEC_WIDTH["size"]),
        ("x_stride", c_uint64, SPEC_WIDTH["stride"]),
        ("y_pad_0", c_uint64, SPEC_WIDTH["pad"]),
        ("y_pad_1", c_uint64, SPEC_WIDTH["pad"]),
        ("x_pad_0", c_uint64, SPEC_WIDTH["pad"]),
        ("x_pad_1", c_uint64, SPEC_WIDTH["pad"]),
    ]


class Instr(Union):
    _fields_ = [("field", InstrBits), ("asbyte", c_uint64)]


instr = Instr()
instr.field.opcode = 0
instr.field.memory_type = 3
instr.field.dram_base = 0x82
instr.y_size = 1
instr.x_size = 1

print(hex(instr.asbyte))


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
