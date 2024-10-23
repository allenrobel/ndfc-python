# [Log]

## Description
Create the base ndfc_python logging object

[Log]: https://github.com/allenrobel/ndfc-python/blob/main/lib/ndfc_python/log_v2.py

## See also

NdfcPythonLogger()

## Raises

- ValueError
  * An error is encountered reading the logging config file.
  * An error is encountered parsing the logging config file.
  * No formatters are found in the logging config file that are associated with the configured handlers.
- TypeError
  * `develop` is not a boolean.

## Methods

`commit()`

:   If `config` is None, disable logging.

    If `config` is a JSON file conformant with `logging.config.dictConfig`
    read the file and configure the base logger instance from the file's contents.

## Properties

`config`

:   Override the `NDFC_LOGGING_CONFIG` environment variable.  Value is an absolute
    path to a JSON file from which logging config is read.  The JSON file must
    conform to `logging.config.dictConfig` from Python's standard library.

    Type: str()

    Default: None

    Raises: None

`develop`

:   Disable or enable exceptions raised by the logging module.

    Type: bool()

    Default: False

    Raises: TypeError if value is not a bool()

## Usage

By default, Log() does the following:

1. Reads the environment variable ``NDFC_LOGGING_CONFIG`` to determine the path
   to the logging config file.  If the environment variable is not set, then
   logging is disabled.
2. Sets ``develop`` to False.  This disables exceptions raised by the logging
   module itself.

### Set environment variable

Set the environment variable `NDFC_LOGGING_CONFIG` to the path of the logging config file.  `bash` shell is used in the example below.

``` bash title="set NDFC_LOGGING_CONFIG"
export NDFC_LOGGING_CONFIG="/path/to/logging_config.json"
```

### Instantiate `Log()`

Instantiate `Log()` and call `commit()` on the instance.

``` py title="instantiate Log()"
import logging
from ndfc_python.log_v2 import Log

try:
    logger = Log()
    logger.commit()
except (TypeError, ValueError) as error:
    print(f"Opps! {error}")
    # handle error
```

At this point, a base/parent logger (`ndfc_python`) is created.  This loggerr is defined in the example logging config file further below.

### Create a logger under `ndfc_python`

``` py title="Create log instance"
log = logging.getLogger("ndfc_python.myLogger")
```

### Start logging

``` py title="Start logging"
log.info("Logger created.")
```

### Disable logging

To disable for all children, unset the environment variable.

```bash
unset NDFC_LOGGING_CONFIG
```

### Enable exceptions

To enable exceptions from the logging module (not recommended, unless needed for development), set ``develop`` to True.

``` py title="set log.develop"
from ndfc_python.log_v2 import Log
try:
    log = Log()
    log.develop = True
    log.commit()
except (TypeError, ValueError) as error:
    # handle error
```

### Override NDFC_LOGGING_CONFIG

To directly set the path to the logging config file, overriding the `NDFC_LOGGING_CONFIG` environment variable, set the `config` property prior to calling `commit()`:

``` py title="Override NDFC_LOGGING_CONFIG"
from ndfc_python.log_v2 import Log
try:
    log = Log()
    log.config = "/path/to/logging_config.json"
    log.commit()
except (TypeError, ValueError) as error:
    # handle error
```

### Example use in a script

``` py
import sys
from ndfc_python.log_v2 import Log

def main():
    try:
        log = Log()
        log.commit()
    except (TypeError, ValueError) as error:
        print(f"Error setting up the logger: {error}")
        sys.exit(1)

    log.info("Scipt started")
```

### Example use in a class

```py title="Example use in a class"
class MyClass:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.log = logging.getLogger(f"ndfc_python.{self.class_name}")
    def some_method(self):
        self.log.debug("This is a debug message.")
```

## Logging Config File

The logging config file must conform to ``logging.config.dictConfig``
from Python's standard library.

An example logging config file is shown below.

``` json title="$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json"
{
  "version": 1,
  "formatters": {
    "standard": {
      "class": "logging.Formatter",
      "format": "%(asctime)s - %(levelname)s - [%(name)s.%(funcName)s.%(lineno)d] %(message)s"
    }
  },
  "handlers": {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "standard",
        "stream"  : "ext://sys.stdout"
      },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "formatter": "standard",
      "filename": "/tmp/ndfc-python.log",
      "mode": "a",
      "encoding": "utf-8",
      "maxBytes": 50000000,
      "backupCount": 4
    }
  },
  "loggers": {
        "ndfc_python": {
        "handlers": [
            "console",
            "file"
        ],
        "level": "DEBUG",
        "propagate": false
        },
        "dcnm": {
            "handlers": [
            "file"
            ],
            "level": "DEBUG",
            "propagate": false
        },
        "root": {
            "level": "INFO",
            "handlers": [
            "file"
            ]
        }
    }
}
```
