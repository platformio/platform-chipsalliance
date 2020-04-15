try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

Import("env")

platform = env.PioPlatform()

# get dirs
fw_dir = os.path.join(platform.get_package_dir("riscv-fw-infrastructure"), "WD-Firmware")
board = env.BoardConfig()
variant_dir = os.path.join(fw_dir, "board", board.get("build.variant", ""))

# read bitstream file option
config = configparser.ConfigParser()
config.read("platformio.ini")
if config.has_option("env:swervolf_nexys", "custom_bitfile"):
    bitfile = config.get("env:swervolf_nexys", "custom_bitfile")
else:
    bitfile = "swervolf_0.bit"

# fpga programming callback
def program_fpga_callback(*args, **kwargs):
    os.chdir(variant_dir)
    env.Execute("./openocd -c \"set BITFILE " + bitfile + "\" -f swervolf_nexys_program.cfg")

# read verilator simulation command option
config = configparser.ConfigParser()
config.read("platformio.ini")
if config.has_option("env:swervolf_sim", "custom_verilator_sim"):
    verilator_sim_cmd = config.get("env:swervolf_sim", "custom_verilator_sim")
else:
    verilator_sim_cmd = "sim/Vswervolf_core_tb +jtag_vpi_enable=1 +ram_init_file=sim/hello.vh"

# verilator simulator callback
def verilator_sim_callback(*args, **kwargs):
    env.Execute(verilator_sim_cmd)

# add new targets
env.AlwaysBuild(env.Alias("program_fpga", None, program_fpga_callback))
env.AlwaysBuild(env.Alias("verilator_sim", None, verilator_sim_callback))