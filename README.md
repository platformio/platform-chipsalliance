# chipsalliance: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-chipsalliance.svg?branch=develop)](https://travis-ci.org/platformio/platform-chipsalliance)
[![Build status](https://ci.appveyor.com/api/projects/status/pm59mq539ttp51hd/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-chipsalliance/branch/develop)

chipsalliance brings the power of open source and software automation to the semiconductor industry, making it possible to develop new hardware faster and more affordably than ever before. 

* [Home](http://platformio.org/platforms/chipsalliance) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/chipsalliance.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

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

Please navigate to [documentation](http://docs.platformio.org/page/platforms/chipsalliance.html).
