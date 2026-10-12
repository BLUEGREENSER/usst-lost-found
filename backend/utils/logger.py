import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(app):
    log_dir = app.config.get("LOG_DIR")
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        handler = TimedRotatingFileHandler(
            os.path.join(log_dir, "app.log"), when="midnight", backupCount=7, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        ))
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    return app.logger