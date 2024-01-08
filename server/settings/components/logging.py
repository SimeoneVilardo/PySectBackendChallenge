LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_error": {
            "level": "WARNING",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/var/www/log/pysect-backend-error.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 365,
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "server": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/var/www/log/pysect-backend-access.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 365,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["server"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file_error", "console"],
        "level": "INFO",
    },
}
