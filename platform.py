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

from os.path import isfile, join

from platformio.managers.platform import PlatformBase


class ChipsalliancePlatform(PlatformBase):
    def get_boards(self, id_=None):
        result = PlatformBase.get_boards(self, id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key, value in result.items():
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get("protocols", [])
        if "tools" not in debug:
            debug["tools"] = {}

        tools = ("digilent-hs1", "ftdi")
        for tool in tools:
            if tool not in upload_protocols or tool in debug["tools"]:
                continue
            server_args = ["-s", "$PACKAGE_DIR/share/openocd/scripts"]
            fw_dir = join("$PROJECT_CORE_DIR", "packages", "riscv-fw-infrastructure")
            board_cfg = join(
                fw_dir, "WD-Firmware", "board", board.get("debug.openocd_config", "")
            )
            if isfile(board_cfg):
                server_args.extend(["-f", board_cfg])
            else:
                assert "Unknown debug configuration", board.id
            debug["tools"][tool] = {
                "server": {
                    "package": "tool-openocd-riscv",
                    "executable": "bin/openocd",
                    "arguments": server_args,
                },
                "onboard": tool in debug.get("onboard_tools", []),
            }

        board.manifest["debug"] = debug
        return board
