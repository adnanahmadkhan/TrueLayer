import xml.etree.ElementTree as ET
from utils.logger import LOG
from utils.util import extract_gz
import time
from parse_movies import df as movies
import json
from init_db import create_database_environment
create_database_environment()
from utils.conn_pool import get_cursor
from pathlib import Path

# loading environment
with open("env.json") as config_json:
    config = json.load(config_json)

start_time = time.time()


my_file = Path(f"{config['wikifile']}")
if not my_file.is_file():
    LOG.info("::Extracting wikipedia gz file::")
    extract_gz(f"{config['wikifile']}.gz")
    LOG.info("::Extraction Complete::")
    print("Archive Extraction time --- Total Time:: %s seconds ---" % (time.time() - start_time))
    LOG.info("Extraction time --- Total Time:: %s seconds ---" % (time.time() - start_time))
else:
    LOG.info("::No Need for extraction - file already present::")

dbfile = config["wikifile"]

wiki_table = {}
insert_stmt = """INSERT INTO final (title, budget, revenue, ratio, release_date, url, abstract, production_companies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

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
    null_titles = 0
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
                if title in wiki_table:
                    null_titles+=1
                wiki_table[title] = {"url": url, "abstract":  abstract}
            else:
                null_titles += 1
except Exception as err:
    LOG.info("Length of Wiki database is:: "+ str(len(wiki_table)))
    LOG.info("Number of empty/null titles is:: "+ str(null_titles))
    if err:
        print(err)

send_to_database = []

# joining titles in movies to titles in the wikipedia database
LOG.info("Joining titles in movies to titles in the wikipedia database")
for index, row in movies.iterrows():
    # avatar 2: amazing movie (2017 film)
    title_to_search = f"{row['title']} ({row['release_date'][:4]} film)"
    if title_to_search in wiki_table:
        # LOG.debug(row["title"])
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue

    # avatar 2: amazing movie (film)
    title_to_search = f"{row['title']} (film)"
    if title_to_search in wiki_table:
        # LOG.debug(row["title"])
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue
    
    # avatar 2: amazing movie
    title_to_search = f"{row['title']}"
    if title_to_search in wiki_table:
        # LOG.debug(row["title"])
        send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
        continue
    
    # avatar 2 (2017 film)
    try:
        title_to_search = f"{row['title']}".split(":")[0] + f" ({row['release_date'][:4]} film)"
        if title_to_search in wiki_table:
            # LOG.debug(row["title"])
            send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
            continue
    except:
        pass

    # avatar 2 (film)
    try:
        title_to_search = f"{row['title']}".split(":")[0] + f" (film)"
        if title_to_search in wiki_table:
            # LOG.debug(row["title"])
            send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
            continue
    except:
        pass

    # avatar 2
    try:
        title_to_search = f"{row['title']}".split(":")[0]
        if title_to_search in wiki_table:
            # LOG.debug(row["title"])
            send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], wiki_table[title_to_search]['url'], wiki_table[title_to_search]['abstract'], row['production_companies']))
            continue
    except:
        pass

    # if title not found in wikipedia, just send to database without wikipedia fields
    send_to_database.append((row['title'], row['budget'], row['revenue'], row['ratio'], row['release_date'], "", "", row['production_companies']))
    LOG.debug("Title not found::"+str(row["title"]))

# push records into database
LOG.info("Saving results to database")
with get_cursor() as cursor:
    cursor.executemany(insert_stmt, send_to_database)

print("Done & Dusted --- Total Time:: %s seconds ---" % (time.time() - start_time))
LOG.info("Done & Dusted --- Total Time:: %s seconds ---" % (time.time() - start_time))