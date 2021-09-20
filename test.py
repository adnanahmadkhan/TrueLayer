from psycopg2 import connect
dbname = "truelayer"
conn = connect(user ='postgres', database=dbname, host = 'localhost', password = 'root', port=5432)

cur = conn.cursor()

cur.execute("select count(*) from wiki")
print(cur.fetchall())

cur.close()
conn.close()