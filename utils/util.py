import gzip
import shutil
import csv
from psycopg2 import Error, DatabaseError
import json

def extract_gz(filename):
    with gzip.open(filename, 'rb') as f_in:
        with open(filename[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def dict_to_csv(dict_data, csv_file, csv_columns):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def run_commands(conn, commands):
    try:
        # read the connection parameters
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        cur.execute("commit")
        # close communication with the PostgreSQL database server
        cur.close()   
    except (Exception, DatabaseError, Error) as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()

def normalize_production_companies(record):
        try:
            record = json.loads(str(record).replace("\'", "\""))
        except:
            return ""
        result = "/".join([x["name"] if "name" in x else "" for x in record])
        return result

