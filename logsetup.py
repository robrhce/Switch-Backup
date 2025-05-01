import logging
import os
import sys

try:
    from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
    has_loki = True
except ImportError:
    has_loki = False

# Create global logger
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

# Avoid adding duplicate handlers if this file is imported multiple times
if not logger.hasHandlers():
    loki_url = os.environ.get("LOKI_URL", "").strip()

    if has_loki and loki_url:
        # Create and attach Loki handler
        custom_handler = LokiLoggerHandler(
            url=loki_url,
            labels={"application": "switch-backup"},
            label_keys={},
            timeout=10,
        )
        logger.addHandler(custom_handler)
        logger.debug("Loki handler attached", extra={'setup': 'true'})
    else:
        # Fallback: log to stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.warning("LOKI_URL not set or LokiLoggerHandler unavailable — using stdout")

# Example usage:
logger.debug("Logger ready", extra={'custom_field': 'custom_value'})