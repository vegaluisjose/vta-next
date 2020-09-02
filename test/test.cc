#include <vta/driver.h>
#include <vta/hw_spec.h>
#include <stdio.h>

void print_instr(VTAGemInsn* instr) {
    uint8_t total = sizeof(VTAGenericInsn);
    uint8_t* bytes = reinterpret_cast<uint8_t*>(instr);
    for (int i = 0; i < total; i++) {
        printf("%02x", bytes[total-i-1]);
    }
    printf("\n");
}

int main() {
    uint32_t num_instr = 1;
    uint32_t wait_cycles = 1000;
    void* buf;
    VTADeviceHandle handle;

    handle = VTADeviceAlloc();
    buf = VTAMemAlloc(sizeof(VTAGemInsn)*num_instr, 0);

    VTAGemInsn* instr = reinterpret_cast<VTAGemInsn*>(buf);

    instr[0].opcode = VTA_OPCODE_FINISH;
    instr[1].opcode = VTA_OPCODE_GEMM;

    print_instr(&instr[0]);
    print_instr(&instr[1]);

    VTADeviceRun(handle, VTAMemGetPhyAddr(buf), num_instr, wait_cycles);

    VTAMemFree(buf);
    VTADeviceFree(handle);

    return 0;
}