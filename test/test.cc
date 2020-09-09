#include <vta/driver.h>
#include <vta/hw_spec.h>
#include <stdio.h>

int main() {
    uint32_t num_instr = 4;
    uint32_t num_bytes = 1024;
    uint32_t wait_cycles = 1000;
    void* instr_buf;
    void* data_buf;
    VTADeviceHandle handle;

    handle = VTADeviceAlloc();
    instr_buf = VTAMemAlloc(sizeof(VTAGenericInsn)*num_instr, 0);
    data_buf = VTAMemAlloc(sizeof(uint8_t)*num_bytes, 0);

    uint32_t* mem32 = reinterpret_cast<uint32_t*>(data_buf);
    uint8_t* mem = reinterpret_cast<uint8_t*>(data_buf);

    uint32_t inp_offset = 2;
    uint32_t out_offset = 1;

    for (int i = 0; i < (num_bytes/4); i++) {
        mem32[i] = i;
    }

    VTAMemInsn* instr_mem = reinterpret_cast<VTAMemInsn*>(instr_buf);
    VTAAluInsn* instr_alu = reinterpret_cast<VTAAluInsn*>(instr_buf);
    VTAGemInsn* instr_gem = reinterpret_cast<VTAGemInsn*>(instr_buf);

    instr_mem[0].opcode = VTA_OPCODE_LOAD;
    instr_mem[0].memory_type = VTA_MEM_ID_ACC;
    instr_mem[0].sram_base = 0;
    instr_mem[0].dram_base = VTAMemGetPhyAddr(data_buf) / VTA_ACC_ELEM_BYTES + inp_offset;
    instr_mem[0].y_size = 1;
    instr_mem[0].x_size = 1;
    instr_mem[0].x_stride = 0;
    instr_mem[0].pop_prev_dep = 0;
    instr_mem[0].pop_next_dep = 0;
    instr_mem[0].push_prev_dep = 0;
    instr_mem[0].push_next_dep = 0;
    instr_mem[0].y_pad_0 = 0;
    instr_mem[0].y_pad_1 = 0;
    instr_mem[0].x_pad_0 = 0;
    instr_mem[0].x_pad_1 = 0;

    instr_alu[1].opcode = VTA_OPCODE_ALU;
    instr_alu[1].alu_opcode = VTA_ALU_OPCODE_SHR;
    instr_alu[1].uop_bgn = 0;
    instr_alu[1].uop_end = 1;
    instr_alu[1].use_imm = true;
    instr_alu[1].imm = 0;
    instr_alu[1].pop_prev_dep = 0;
    instr_alu[1].pop_next_dep = 0;
    instr_alu[1].push_prev_dep = 0;
    instr_alu[1].push_next_dep = 1;
    instr_alu[1].iter_in = 1;
    instr_alu[1].iter_out = 1;
    instr_alu[1].reset_reg = false;
    instr_alu[1].dst_factor_out = 0;
    instr_alu[1].src_factor_out = 0;
    instr_alu[1].dst_factor_in = 0;
    instr_alu[1].src_factor_in = 0;

    instr_mem[2].opcode = VTA_OPCODE_STORE;
    instr_mem[2].memory_type = VTA_MEM_ID_OUT;
    instr_mem[2].sram_base = 0;
    instr_mem[2].dram_base = VTAMemGetPhyAddr(data_buf) / VTA_OUT_ELEM_BYTES + out_offset;
    instr_mem[2].y_size = 1;
    instr_mem[2].x_size = 1;
    instr_mem[2].pop_prev_dep = 1;
    instr_mem[2].pop_next_dep = 0;
    instr_mem[2].push_prev_dep = 1;
    instr_mem[2].push_next_dep = 0;
    instr_mem[2].x_stride = 0;
    instr_mem[2].y_pad_0 = 0;
    instr_mem[2].y_pad_1 = 0;
    instr_mem[2].x_pad_0 = 0;
    instr_mem[2].x_pad_1 = 0;

    instr_gem[3].opcode = VTA_OPCODE_FINISH;
    instr_gem[3].pop_prev_dep = 0;
    instr_gem[3].pop_next_dep = 1;
    instr_gem[3].push_prev_dep = 0;
    instr_gem[3].push_next_dep = 0;

    for (int i = 0; i < (VTA_ACC_ELEM_BYTES/4); i++) {
        printf("i[%02d]:%08x\n", i, mem32[i+(VTA_ACC_ELEM_BYTES/4)*inp_offset]);
    }

    VTADeviceRun(handle, VTAMemGetPhyAddr(instr_buf), num_instr, wait_cycles);

    for (int i = 0; i < VTA_OUT_ELEM_BYTES; i++) {
        printf("o[%02d]:%02x\n", i, mem[i+VTA_OUT_ELEM_BYTES*out_offset]);
    }

    VTAMemFree(instr_buf);
    VTAMemFree(data_buf);
    VTADeviceFree(handle);

    return 0;
}