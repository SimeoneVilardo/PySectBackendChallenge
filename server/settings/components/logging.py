LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/var/www/log/pysect-backend.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 365,
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}
