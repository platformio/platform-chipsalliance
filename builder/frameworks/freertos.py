# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FIRMWARE_DIR = platform.get_package_dir("framework-wd-riscv-sdk")
assert os.path.isdir(FIRMWARE_DIR)

if "wd-riscv-sdk" not in env.subst("$PIOFRAMEWORK"):
    # Force SDK package to build if only FreeRTOS is specified in framework list
    env.SConscript("wd-riscv-sdk.py")

env.Append(
    CPPDEFINES=[
        "D_USE_RTOSAL",
        "D_USE_FREERTOS"
    ],

    CPPPATH=[
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "loc_inc"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "api_inc"),
        os.path.join(FIRMWARE_DIR, "rtos", "rtosal", "config", "eh1"),
        os.path.join(
            FIRMWARE_DIR, "rtos", "rtos_core", "freertos", "Source", "include"),
    ],

    LIBS=[
        env.BuildLibrary(
            os.path.join("$BUILD_DIR", "RTOS-AL"),
            os.path.join(FIRMWARE_DIR, "rtos", "rtosal"),
            src_filter="+<*> -<rtosal_memory.c> -<list.c>"
        ),
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
            ]
        )
    ]
)
