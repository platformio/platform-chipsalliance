How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](https://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/platformio/platform-chipsalliance/archive/develop.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-chipsalliance/examples/native-blink_asm

# Build project
$ pio run

# Upload firmware
$ pio run --target upload

# Upload bitstream
$ pio run --target program_fpga

# Generate trace for GTKWave
$ pio run --target generate_trace

# Start verilator as JTAG server for OpenOCD
$ pio run --target start_verilator

# Generate bistream for SweRV Core using Xilinx Vivado
$ pio run --target generate_bitstream

# Upload firmware for the specific environment
$ pio run -e swervolf_nexys --target upload

# Clean build files
$ pio run --target clean
```
