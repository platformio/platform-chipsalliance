#define LEDs_ADDR    0x80001010
#define SWs_ADDR    0x80001012

.globl _start
_start:

next:
    li  a1, SWs_ADDR         # Read the Switches
    lw  t0, 0(a1)
 
    li  a0, LEDs_ADDR        # Write the LEDs
    sw  t0, 0(a0)
 
    beq zero, zero, next     # infinite loop

.end 
