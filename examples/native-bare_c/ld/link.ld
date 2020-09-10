OUTPUT_ARCH( "riscv" )
ENTRY(_start)

SECTIONS
{
  . = 0;
  .text : { *(.text*) }
  .rodata : { *(.rodata*) }
  .bss : { *(.bss*) }
}
