import logging

logging.basicConfig(
    filename="log/backfill.log",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
)
LOG = logging.getLogger()
