import xml.etree.ElementTree as ET
from utils.conn_pool import get_cursor
from utils.logger import LOG
import time
from parse_movies import df as movies
# from init_db import create_database_environment
# create_database_environment()

start_time = time.time()

dbfile = "./data/enwiki-latest-abstract.xml"
# dbfile = "./data/test.xml"

wiki_table = {}
insert_stmt = """INSERT INTO final (title, budget, revenue, ratio, release_date, url, abstract, production_companies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (title) DO NOTHING"""

LOG.info("Getting an iterator to iterate over the XML database")
# get an iterable
context = ET.iterparse(dbfile, events=("start", "end"))

# turn it into an iterator
context = iter(context)

# get the root element
event, root = context.__next__()


# just iterating over the XML file and fetching all titles; 
# its corresponding url & abstract fields.
# And finally, putting them in a dictionary

LOG.info("Iterating over the XML database and collecting necessary stats")
try:
    while event:
        title = url = abstract = ""
        (event, elem) = context.__next__()
        url_found = abstract_found = False
        if event == "end" and elem.tag == "title":
            title = str(elem.text).replace("Wikipedia:", "").strip().lower()
            while not url_found or not abstract_found:
                (event, elem) = context.__next__()
                if event == "end" and elem.tag == "url":
                    url = str(elem.text).strip()
                    url_found = True
                if event == "end" and elem.tag == "abstract":
                    abstract = str(elem.text).strip()
                    abstract_found = True
                elif event == "end" and elem.tag == "title":
                    break
                root.clear()
            if title not in ["", None]:
                wiki_table[title] = {"url": url, "abstract":  abstract}
except Exception as err:
    if err:
        print(err)

send_to_database = []

# joining titles in movies to titles in the wikipedia database
LOG.info("Joining titles in movies to titles in the wikipedia database")
for index, row in movies.iterrows():
    title_to_search = f"{row['title']} ({row['release_date'][:4]} film)"
    if title_to_search in wiki_table:
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue

    title_to_search = f"{row['title']} (film)"
    if title_to_search in wiki_table:
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue
    
    title_to_search = f"{row['title']}"
    if title_to_search in wiki_table:
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue

# push records into database
LOG.info("Saving results to database")
with get_cursor() as cursor:
    cursor.executemany(insert_stmt, send_to_database)

print("Done & Dusted --- %s seconds ---" % (time.time() - start_time))