import multiprocessing
from os import environ

# ----------------------------------------------------------------
# Gunicorn basic configuration file
# ----------------------------------------------------------------
# Bind to port on all interfaces
bind = environ.get("GUNICORN_BIND", "0.0.0.0:5000")

# Worker processes
cores = multiprocessing.cpu_count()
# Limit to 4 cores or less
if cores > 4:
    cores = 4
workers = int(environ.get("GUNICORN_WORKERS", cores))
worker_class = environ.get("GUNICORN_WORKER_CLASS", "sync")  # "sync" | "gthread"
# threads = int(environ.get("GUNICORN_THREADS", cores * 2))

# Preload the app to leverage copy-on-write
preload_app = True


# ----------------------------------------------------------------
# Custom logging configuration
# ----------------------------------------------------------------
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [PID:%(process)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %Z]",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },

    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },

    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
# This takes precedence over --log-config and --log-config-json and uses Python's standard dictConfig style.
logconfig_dict = logconfig_dict

# Access and error logs
accesslog = environ.get("GUNICORN_ACCESS_LOG", "-")
errorlog = environ.get("GUNICORN_ERROR_LOG", "-")
loglevel = environ.get("GUNICORN_LOG_LEVEL", "info")
capture_output = True
access_log_format = '%(r)s [STATUS:%(s)s] [%(M)sms]'
