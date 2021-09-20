import json
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from utils.logger import LOG

with open("env.json") as config_json:
    config = json.load(config_json)

LOG.info(f'Initializing connection pool')
db = SimpleConnectionPool(1, 10, host=config["hostname"], database=config["dbname"],user=config["dbuser"],password=config["password"],port=config["port"])

# Get Cursor
@contextmanager
def get_cursor():
    con = db.getconn()
    try:
        yield con.cursor()
        con.commit()
    finally:
        db.putconn(con)
