import sys
from datetime import datetime

from db.connection import Pg8000Connection
from etl import etl_backfill
from services import reset_db

# dangerous!
if False:
    reset_db(Pg8000Connection())

# backfill based on input dates
etl_backfill(
    datetime(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])),
    datetime(int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])),
)
