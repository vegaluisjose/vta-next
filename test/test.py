from ctypes import c_uint64, c_uint8, Structure, Union

# uop_begin, uop_end and *_factor are derived from config
width = {
    "flag": 1,
    "opcode": 3,
    "alu_opcode": 2,
    "imm": 16,
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
        ("pop_prev_dep", c_uint64, width["flag"]),
        ("pop_next_dep", c_uint64, width["flag"]),
        ("push_prev_dep", c_uint64, width["flag"]),
        ("push_next_dep", c_uint64, width["flag"]),
        ("memory_type", c_uint64, width["memory_type"]),
        ("sram_addr", c_uint64, width["sram_addr"]),
        ("dram_addr", c_uint64, width["dram_addr"]),
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

    def __init__(self, op_type, mem_type):
        try:
            assert op_type != "gemm"
            assert op_type != "finish"
            assert op_type != "alu"
            self.field.opcode = opcode[op_type]
        except KeyError:
            print("~~~>{} operation is not supported".format(op_type))
            raise
        try:
            self.field.memory_type = memory_type[mem_type]
        except KeyError:
            print("~~~>{} memory type is not supported".format(mem_type))
            raise

    def __str__(self):
        return serialize_instr(self)

    def set_addr(self, type, value):
        valid = type == "sram" or type == "dram"
        assert valid
        if type == "sram":
            self.field.sram_addr = value
        else:
            self.field.dram_addr = value

    def set_size(self, type, value):
        valid = type == "x" or type == "y"
        assert valid
        if type == "x":
            self.field.x_size = value
        else:
            self.field.y_size = value

    def set_stride(self, type, value):
        valid = type == "x"
        assert valid
        self.field.x_stride = value

    def set_pad(self, type, value):
        valid = type == "x0" or type == "y0" or type == "x1" or type == "y1"
        assert valid
        if type == "x0":
            self.field.x_pad_0 = value
        elif type == "y0":
            self.field.y_pad_0 = value
        elif type == "x1":
            self.field.x_pad_1 = value
        else:
            self.field.y_pad_1 = value

    def pop_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.pop_prev_dep = 1
        else:
            self.field.pop_next_dep = 1

    def push_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.push_prev_dep = 1
        else:
            self.field.push_next_dep = 1


class AluInstrBits(Structure):
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint64, width["opcode"]),
        ("pop_prev_dep", c_uint64, width["flag"]),
        ("pop_next_dep", c_uint64, width["flag"]),
        ("push_prev_dep", c_uint64, width["flag"]),
        ("push_next_dep", c_uint64, width["flag"]),
        ("reset", c_uint64, width["flag"]),
        ("uop_begin", c_uint64, width["uop_begin"]),
        ("uop_end", c_uint64, width["uop_end"]),
        ("iter_out", c_uint64, width["iter"]),
        ("iter_in", c_uint64, width["iter"]),
        ("dst_factor_out", c_uint64, width["dst_factor"]),
        ("dst_factor_in", c_uint64, width["dst_factor"]),
        ("src_factor_out", c_uint64, width["src_factor"]),
        ("src_factor_in", c_uint64, width["src_factor"]),
        ("alu_opcode", c_uint64, width["alu_opcode"]),
        ("use_imm", c_uint64, width["flag"]),
        ("imm", c_uint64, width["imm"]),
    ]


class AluInstr(Union):
    _fields_ = [("field", AluInstrBits), ("asbyte", InstrBytes)]

    def __init__(self, op_type):
        self.field.opcode = opcode["alu"]
        try:
            self.field.alu_opcode = alu_opcode[op_type]
        except KeyError:
            print("~~~>{} alu operation is not supported".format(op_type))
            raise

    def __str__(self):
        return serialize_instr(self)

    def set_reset(self):
        self.field.reset = 1

    def clear_reset(self):
        self.field.reset = 0

    def set_imm_flag(self):
        self.field.use_imm = 1

    def clear_imm_flag(self):
        self.field.use_imm = 0

    def set_imm(self, value):
        self.set_imm_flag()
        self.field.imm = value

    def set_uop(self, type, value):
        valid = type == "begin" or type == "end"
        assert valid
        if type == "begin":
            self.field.uop_begin = value
        else:
            self.field.uop_end = value

    def set_iter(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.iter_in = value
        else:
            self.field.iter_out = value

    def set_dst(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.dst_factor_in = value
        else:
            self.field.dst_factor_out = value

    def set_src(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.src_factor_in = value
        else:
            self.field.src_factor_out = value

    def pop_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.pop_prev_dep = 1
        else:
            self.field.pop_next_dep = 1

    def push_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.push_prev_dep = 1
        else:
            self.field.push_next_dep = 1


class GemInstrBits(Structure):
    _pack_ = 1
    _fields_ = [
        ("opcode", c_uint64, width["opcode"]),
        ("pop_prev_dep", c_uint64, width["flag"]),
        ("pop_next_dep", c_uint64, width["flag"]),
        ("push_prev_dep", c_uint64, width["flag"]),
        ("push_next_dep", c_uint64, width["flag"]),
        ("reset", c_uint64, width["flag"]),
        ("uop_begin", c_uint64, width["uop_begin"]),
        ("uop_end", c_uint64, width["uop_end"]),
        ("iter_out", c_uint64, width["iter"]),
        ("iter_in", c_uint64, width["iter"]),
        ("dst_factor_out", c_uint64, width["dst_factor"]),
        ("dst_factor_in", c_uint64, width["dst_factor"]),
        ("src_factor_out", c_uint64, width["src_factor"]),
        ("src_factor_in", c_uint64, width["src_factor"]),
        ("wgt_factor_out", c_uint64, width["wgt_factor"]),
        ("wgt_factor_in", c_uint64, width["wgt_factor"]),
    ]


class GemInstr(Union):
    _fields_ = [("field", GemInstrBits), ("asbyte", InstrBytes)]

    def __init__(self, op_type):
        try:
            assert op_type != "load"
            assert op_type != "store"
            assert op_type != "alu"
            self.field.opcode = opcode[op_type]
        except KeyError:
            print("~~~>{} operation is not supported".format(op_type))
            raise

    def __str__(self):
        return serialize_instr(self)

    def set_reset(self):
        self.field.reset = 1

    def clear_reset(self):
        self.field.reset = 0

    def set_uop(self, type, value):
        valid = type == "begin" or type == "end"
        assert valid
        if type == "begin":
            self.field.uop_begin = value
        else:
            self.field.uop_end = value

    def set_iter(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.iter_in = value
        else:
            self.field.iter_out = value

    def set_dst(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.dst_factor_in = value
        else:
            self.field.dst_factor_out = value

    def set_src(self, type, value):
        valid = type == "in" or type == "out"
        assert valid
        if type == "in":
            self.field.src_factor_in = value
        else:
            self.field.src_factor_out = value

    def pop_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.pop_prev_dep = 1
        else:
            self.field.pop_next_dep = 1

    def push_dep(self, type):
        valid = type == "prev" or type == "next"
        assert valid
        if type == "prev":
            self.field.push_prev_dep = 1
        else:
            self.field.push_next_dep = 1


class Prog(object):
    def __init__(self, name):
        self.name = name
        self.body = []

    def __str__(self):
        body = ["{}".format(instr) for instr in self.body]
        return "\n".join(body)

    def add_instr(self, instr):
        self.body.append(instr)


def create_prog(name):
    load = MemInstr("load", "acc")
    alu = AluInstr("add")
    store = MemInstr("store", "out")
    finish = GemInstr("finish")
    load.set_addr("dram", 130)
    load.set_size("y", 1)
    load.set_size("x", 1)
    alu.set_uop("end", 1)
    alu.set_imm(0)
    alu.push_dep("next")
    alu.set_iter("in", 1)
    alu.set_iter("out", 1)
    store.set_addr("dram", 513)
    store.set_size("y", 1)
    store.set_size("x", 1)
    store.pop_dep("prev")
    store.push_dep("prev")
    finish.pop_dep("next")
    prog = Prog(name)
    prog.add_instr(load)
    prog.add_instr(alu)
    prog.add_instr(store)
    prog.add_instr(finish)
    return prog


if __name__ == "__main__":
    prog = create_prog("test")
    print(prog)
