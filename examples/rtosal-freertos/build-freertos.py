import os

Import("env")

# Note: "riscv-fw-infrastructure" repository contains toolchains and eclipse
FW_DIR = os.path.join(
    "$PROJECT_CORE_DIR", "packages", "riscv-fw-infrastructure", "WD-Firmware"
)

board = env.BoardConfig()
variant_dir = os.path.join(FW_DIR, "board", board.get("build.variant", ""))

env.Append(
    ASFLAGS=[
        "-x", "assembler-with-cpp",
        "-Wa,-march=%s" % board.get("build.march")
    ],

    CCFLAGS=[
        "-Os",
        "-Wall",
        "-ffunction-sections",
        "-fdata-sections",
        "-march=%s" % board.get("build.march"),
        "-mabi=%s" % board.get("build.mabi"),
        "-mcmodel=%s" % board.get("build.mcmodel"),
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
        os.path.join(FW_DIR, "rtos", "rtosal", "loc_inc"),
        os.path.join(FW_DIR, "common", "api_inc"),
        os.path.join(FW_DIR, "rtos", "rtos_core", "freertos", "Source", "include"),
        os.path.join(FW_DIR, "rtos", "rtosal", "api_inc"),
        os.path.join(FW_DIR, "rtos", "rtosal", "config", "swerv_eh1"),
        os.path.join(FW_DIR, "psp", "api_inc"),
        os.path.join(FW_DIR, "rtos", "rtos_core", "freertos", "Source", "include"),
    ],

    LINKFLAGS=[
        "-Os",
        "-march=%s" % board.get("build.march"),
        "-mabi=%s" % board.get("build.mabi"),
        "-mcmodel=%s" % board.get("build.mcmodel"),
        "-Wl,-gc-sections",
        "-nostdlib",
        "-nostartfiles",
        "-static",
        "-Wl,--wrap=malloc",
        "-Wl,--wrap=free",
        "-Wl,--wrap=open",
        "-Wl,--wrap=lseek",
        "-Wl,--wrap=read",
        "-Wl,--wrap=write",
        "-Wl,--wrap=fstat",
        "-Wl,--wrap=stat",
        "-Wl,--wrap=close",
        "-Wl,--wrap=link",
        "-Wl,--wrap=unlink",
        "-Wl,--wrap=execve",
        "-Wl,--wrap=fork",
        "-Wl,--wrap=getpid",
        "-Wl,--wrap=kill",
        "-Wl,--wrap=wait",
        "-Wl,--wrap=isatty",
        "-Wl,--wrap=times",
        "-Wl,--wrap=sbrk",
        "-Wl,--wrap=_exit"
        "-Wl,-Map="
        + os.path.join("$BUILD_DIR", os.path.basename(env.subst("${PROJECT_DIR}.map"))),
        "-Wl,--defsym=__comrv_cache_size=0",
    ],

    LIBPATH=[variant_dir],

    LIBS=["c", "gcc"]
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

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
        os.path.join(FW_DIR, "rtos", "rtos_core", "freertos", "Source"),
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
        os.path.join(FW_DIR, "rtos", "rtosal"),
        src_filter="+<*> -<rtosal_memory.c> -<list.c>",
    ),

    env.BuildLibrary(
        os.path.join("$BUILD_DIR", "PSP"),
        os.path.join(FW_DIR, "psp"),
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
