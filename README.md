# CHIPS Alliance: development platform for [PlatformIO](http://platformio.org)

[![Build Status](https://github.com/platformio/platform-chipsalliance/workflows/Examples/badge.svg)](https://github.com/platformio/platform-chipsalliance/actions)

CHIPS Alliance brings the power of open source and software automation to the semiconductor industry, making it possible to develop new hardware faster and more affordably than ever before.

* [Home](https://registry.platformio.org/platforms/platformio/chipsalliance) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/chipsalliance.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = chipsalliance
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-chipsalliance.git
board = ...
...
```

# Configuration

Please navigate to [documentation](https://docs.platformio.org/page/platforms/chipsalliance.html).
