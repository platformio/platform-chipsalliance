import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FIRMWARE_DIR = platform.get_package_dir("framework-wd-riscv-sdk")
assert os.path.isdir(FIRMWARE_DIR)

board = env.BoardConfig()
variant_dir = os.path.join(FIRMWARE_DIR, "board", board.get("build.variant", ""))

env.SConscript("_bare.py")

env.Append(
    CCFLAGS=[
        "-fno-builtin-printf",
    ],

    CPPDEFINES=[
        ("D_TICK_TIME_MS", 4),
        ("D_ISR_STACK_SIZE", 400),
        ("D_MTIME_ADDRESS", "0x80001020"),
        ("D_MTIMECMP_ADDRESS", "0x80001028"),
        ("D_CLOCK_RATE", 50000000),
        ("D_PIC_BASE_ADDRESS", "0xF00C0000"),
        ("D_PIC_NUM_OF_EXT_INTERRUPTS", 256),
        ("D_EXT_INTERRUPT_FIRST_SOURCE_USED", 0),
        ("D_EXT_INTERRUPT_LAST_SOURCE_USED", 255),
        ("D_EXT_INTS_GENERATION_REG_ADDRESS", "0x8000100B"),
        ("D_TIMER_DURATION_SETUP_ADDRESS", "0x80001030"),
        ("D_TIMER_ACTIVATION_ADDRESS", "0x80001034"),
        ("D_NMI_VEC_ADDRESSS", "0x8000100C")
    ],

    CPPPATH=[
        "$PROJECT_SRC_DIR",
        os.path.join(FIRMWARE_DIR, "common", "api_inc"),
        os.path.join(FIRMWARE_DIR, "psp", "api_inc")
    ],

    LIBPATH=[variant_dir],

    LIBS=["c", "gcc"]
)

if not any(rtos in env.subst("$PIOFRAMEWORK") for rtos in ("freertos", "threadx")):
    env.Append(CPPDEFINES=["D_BARE_METAL"])

# Only for C/C++ sources
env.Append(CCFLAGS=["-includesys/cdefs.h"])

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH="link.lds")

#
# Target: Build libraries
#

libs = []

if "build.variant" in board:
    env.Append(CPPPATH=[variant_dir, os.path.join(variant_dir, "bsp")])
    libs.append(env.BuildLibrary(os.path.join("$BUILD_DIR", "BoardBSP"), variant_dir))

libs.append(
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "PSP"),
        os.path.join(FIRMWARE_DIR, "psp"),
        src_filter=[
            "-<*>",
            "+<psp_version.c>",
            "+<psp_interrupts_eh1.c>",
            "+<psp_ext_interrupts_eh1.c>",
            "+<psp_timers_eh1.c>",
            "+<psp_pmc_eh1.c>",
            "+<psp_performance_monitor_eh1.c>",
            "+<psp_nmi_eh1.c>",
            "+<psp_corr_err_cnt_eh1.c>",
            "+<psp_int_vect_eh1.S>"
        ]
    )
)

env.Prepend(LIBS=libs)
