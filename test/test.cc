#include <vta/driver.h>
#include <vta/hw_spec.h>
#include <stdio.h>

int main() {
    uint32_t num_instr = 1;
    uint32_t wait_cycles = 1000;
    void* buf;
    VTADeviceHandle handle;

    handle = VTADeviceAlloc();
    buf = VTAMemAlloc(sizeof(VTAGemInsn)*num_instr, 0);

    VTAGemInsn* instr = reinterpret_cast<VTAGemInsn*>(buf);
    instr[0].opcode = VTA_OPCODE_FINISH;

    VTADeviceRun(handle, VTAMemGetPhyAddr(buf), num_instr, wait_cycles);

    VTAMemFree(buf);
    VTADeviceFree(handle);

    return 0;
}