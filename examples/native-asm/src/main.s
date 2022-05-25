.globl _start
_start:

next:
    li  a1, 0x80001012         # Read the Switches
    lw  t0, 0(a1)

    li  a0, 0x80001010        # Write the LEDs
    sw  t0, 0(a0)

    beq zero, zero, next     # infinite loop

.end
