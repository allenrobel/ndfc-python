# Enable logging

If you want to enable script logging (optional), set the following environment variable.

```bash
export NDFC_LOGGING_CONFIG=$HOME/repos/ndfc-python/lib/ndfc_python/logging_config.json
```

`NDFC_LOGGING_CONFIG` should point to a standard Pyton logging configuration file.  There is an example file in this repository at ``lib/ndfc_python/logging_config.json``.  Below is the contents.

``` json title="Example logging configuration file"
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
            "console",
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
