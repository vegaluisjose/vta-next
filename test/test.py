from ctypes import c_uint64, c_uint8, Structure, Union

# uop_begin, uop_end and *_factor are derived from config
width = {
    "opcode": 3,
    "alu_opcode": 2,
    "use_imm": 1,
    "imm": 16,
    "pop_push": 1,
    "reset": 1,
    "memory_type": 2,
    "sram_addr": 16,
    "dram_addr": 32,
    "size": 16,
    "stride": 16,
    "pad": 4,
    "uop_begin": 13,
    "uop_end": 14,
    "iter": 14,
    "dst_factor": 11,
    "src_factor": 11,
    "wgt_factor": 10,
}

opcode = {
    "load": 0,
    "store": 1,
    "gemm": 2,
    "finish": 3,
    "alu": 4,
}

alu_opcode = {
    "min": 0,
    "max": 1,
    "add": 2,
    "shr": 3,
}

memory_type = {
    "uop": 0,
    "wgt": 1,
    "inp": 2,
    "acc": 3,
    "out": 4,
}

InstrBytes = c_uint8 * 16

def serialize_instr(instr):
    x = list(bytes(instr.asbyte))
    x.reverse()
    y = ["{:02x}".format(i) for i in x]
    return "".join(y)

class MemInstrBits(Structure):
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint64, width["opcode"]),
        ("pop_prev_dep", c_uint64, width["pop_push"]),
        ("pop_next_dep", c_uint64, width["pop_push"]),
        ("push_prev_dep", c_uint64, width["pop_push"]),
        ("push_next_dep", c_uint64, width["pop_push"]),
        ("memory_type", c_uint64, width["memory_type"]),
        ("sram_base", c_uint64, width["sram_addr"]),
        ("dram_base", c_uint64, width["dram_addr"]),
        ("y_size", c_uint64, width["size"]),
        ("x_size", c_uint64, width["size"]),
        ("x_stride", c_uint64, width["stride"]),
        ("y_pad_0", c_uint64, width["pad"]),
        ("y_pad_1", c_uint64, width["pad"]),
        ("x_pad_0", c_uint64, width["pad"]),
        ("x_pad_1", c_uint64, width["pad"]),
    ]


class MemInstr(Union):
    _fields_ = [("field", MemInstrBits), ("asbyte", InstrBytes)]

    def __str__(self):
        return serialize_instr(self)


class AluInstrBits(Structure):
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint64, width["opcode"]),
        ("pop_prev_dep", c_uint64, width["pop_push"]),
        ("pop_next_dep", c_uint64, width["pop_push"]),
        ("push_prev_dep", c_uint64, width["pop_push"]),
        ("push_next_dep", c_uint64, width["pop_push"]),
        ("reset", c_uint64, width["reset"]),
        ("uop_begin", c_uint64, width["uop_begin"]),
        ("uop_end", c_uint64, width["uop_end"]),
        ("iter_out", c_uint64, width["iter"]),
        ("iter_in", c_uint64, width["iter"]),
        ("dst_factor_out", c_uint64, width["dst_factor"]),
        ("dst_factor_in", c_uint64, width["dst_factor"]),
        ("src_factor_out", c_uint64, width["src_factor"]),
        ("src_factor_in", c_uint64, width["src_factor"]),
        ("alu_opcode", c_uint64, width["alu_opcode"]),
        ("use_imm", c_uint64, width["use_imm"]),
        ("imm", c_uint64, width["imm"]),
    ]

class AluInstr(Union):
    _fields_ = [("field", AluInstrBits), ("asbyte", InstrBytes)]

    def __str__(self):
        return serialize_instr(self)

class Prog(object):
    def __init__(self, name):
        self.name = name
        self.body = []

    def add_instr(self, instr):
        self.body.append(instr)

def load():
    instr = MemInstr()
    instr.field.opcode = opcode["load"]
    instr.field.memory_type = memory_type["acc"]
    instr.field.dram_base = 0x82
    instr.field.y_size = 1
    instr.field.x_size = 1
    return instr

print(load())
