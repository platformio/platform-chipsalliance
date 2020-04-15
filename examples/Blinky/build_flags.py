Import("env")

# Building flags
env.Append(ASFLAGS=["-march=rv32i", "-mabi=ilp32"])
env.Append(LINKFLAGS=["-nostartfiles","-march=rv32i","-mabi=ilp32"])
