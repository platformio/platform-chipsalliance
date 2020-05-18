import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

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
        "-mcmodel=%s" % board.get("build.mcmodel")
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
    ]
)

# copy CCFLAGS to ASFLAGS (-x assembler-with-cpp mode)
env.Append(ASFLAGS=env.get("CCFLAGS", [])[:])

#
# Target: Build libraries
#
