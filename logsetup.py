# logsetup.py
import logging, os, sys
try:
    from loki_logger import LokiHandler
except ImportError:
    LokiHandler = None

logger = logging.getLogger("backup")
logger.setLevel(logging.INFO)

loki_url = os.environ.get("LOKI_URL", "").strip()

if loki_url and LokiHandler:
    logger.addHandler(LokiHandler(url=loki_url, tags={"job": "switch-backup"}))
else:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)