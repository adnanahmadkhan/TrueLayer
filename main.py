import xml.etree.ElementTree as ET
from utils.conn_pool import get_cursor 
import time
from parse_movies import df as movies

start_time = time.time()

dbfile = "./data/enwiki-latest-abstract.xml"
# dbfile = "./data/test.xml"

wiki_table = []
bulk_size = 20000
insert_stmt = """INSERT INTO wiki (title, url, abstract) VALUES (%s, %s, %s)"""

# get an iterable
context = ET.iterparse(dbfile, events=("start", "end"))

# turn it into an iterator
context = iter(context)

# get the root element
event, root = context.__next__()


try:
    while event:
        title = url = abstract = ""
        (event, elem) = context.__next__()
        url_found = abstract_found = False
        if event == "end" and elem.tag == "title":
            title = str(elem.text).replace("Wikipedia:", "").strip()
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
                wiki_table.append((title, url, abstract))
        # inserting batch into table
        if len(wiki_table) == bulk_size:
            with get_cursor() as cursor:
                cursor.executemany(insert_stmt, wiki_table)
            wiki_table = []
    
except Exception as err:
    print("Error::", err)
    # checking for last batch
    if len(wiki_table) > 0:
        with get_cursor() as cursor:
            cursor.executemany(insert_stmt, wiki_table)


print("Done & Dusted --- %s seconds ---" % (time.time() - start_time))