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
        "D_USE_RTOSAL",
        "D_USE_FREERTOS",
        ("D_TICK_TIME_MS", 4),
        ("D_ISR_STACK_SIZE", 400),
        ("D_MTIME_ADDRESS", "0x80001020"),
        ("D_MTIMECMP_ADDRESS", "0x80001028"),
        ("D_CLOCK_RATE", 50000000),
        ("D_PIC_BASE_ADDRESS", "0xA0000000"),
        ("D_PIC_NUM_OF_EXT_INTERRUPTS", 256),
        ("D_EXT_INTERRUPT_FIRST_SOURCE_USED", 0),
        ("D_EXT_INTERRUPT_LAST_SOURCE_USED", 255),
    ],

    CPPPATH=[
        "$PROJECT_SRC_DIR",
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "loc_inc"),
        os.path.join(FIRMWARE_DIR, "common", "api_inc"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtos_core", "freertos", "Source", "include"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "api_inc"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "config", "swerv_eh1"),
        os.path.join(FIRMWARE_DIR, "psp", "api_inc"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtos_core", "freertos", "Source", "include"),
    ],

    LIBPATH=[variant_dir],

    LIBS=["c", "gcc"]
)

# Only for C/C++ sources
env.Append(CCFLAGS=["-include", "sys/cdefs.h"])

if not board.get("build.ldscript", ""):
    env.Replace(LDSCRIPT_PATH="link.lds")

#
# Target: Build libraries
#

libs = []

if "build.variant" in board:
    env.Append(CPPPATH=[variant_dir, os.path.join(variant_dir, "bsp")])
    libs.append(env.BuildLibrary(os.path.join("$BUILD_DIR", "BoardBSP"), variant_dir))

libs.extend([
    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "FreeRTOS"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtos_core", "freertos", "Source"),
        src_filter=[
            "-<*>",
            "+<croutine.c>",
            "+<list.c>",
            "+<portable/portASM.S>",
            "+<queue.c>",
            "+<tasks.c>",
            "+<timers.c>",
        ],
    ),

    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "RTOS-AL"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal"),
        src_filter="+<*> -<rtosal_memory.c> -<list.c>",
    ),

    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "PSP"),
        os.path.join(FIRMWARE_DIR, "psp"),
        src_filter=[
            "-<*>",
            "+<psp_ext_interrupts_swerv_eh1.c>",
            "+<psp_traps_interrupts.c>",
            "+<psp_timers.c>",
            "+<psp_performance_monitor_eh1.c>",
            "+<psp_int_vect_swerv_eh1.S>"
        ],
    )
])

env.Prepend(LIBS=libs)
