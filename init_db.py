from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
from utils.logger import LOG
from utils.util import run_commands
import json
start_time = time.time()

# loading environment
with open("env.json") as config_json:
    config = json.load(config_json)

LOG.info("::INIT DB STARTED::")

def create_database_environment():
    create_table_stmt = (
        """
        CREATE TABLE final (
                title VARCHAR(255) PRIMARY KEY,
                budget decimal,
                revenue decimal,
                ratio decimal,
                release_date date,
                url VARCHAR(1500),
                abstract VARCHAR(2000),
                production_companies VARCHAR(1500)
                )
        """, )

    LOG.info('connecting to default database')
    con = connect(host=config["hostname"],user=config["dbuser"],password=config["password"],port=config["port"])
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()

    LOG.info(f'Dropping {config["dbname"]} database if exists')
    cur.execute('DROP DATABASE IF EXISTS ' + config["dbname"])

    LOG.info(f'Creating fresh copy of {config["dbname"]} database')
    cur.execute('CREATE DATABASE ' + config["dbname"])
    cur.close()
    con.close()

    LOG.info('Connecting to %s ...' % (config["dbname"]))
    LOG.info(f'Creating final table')
    conn = connect(database=config["dbname"], host=config["hostname"],user=config["dbuser"],password=config["password"],port=config["port"])
    run_commands(conn,create_table_stmt)
    conn.close()

LOG.info(f'::INIT DB COMPLETE::')
LOG.info("Database Environment Created --- %s seconds ---" % (time.time() - start_time))
print("Database Environment Created --- %s seconds ---" % (time.time() - start_time))