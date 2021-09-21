import pandas as pd
from utils import util
from utils.logger import LOG
import json
import time
start_time = time.time()

# loading environment
with open("env.json") as config_json:
    config = json.load(config_json)

movies_file = config["moviesfile"]

LOG.info("Reading movies file with C engine")
# read csv file
df = pd.read_csv(movies_file, engine="c", dtype={"popularity": str})

LOG.info("Converting necessary fields from strings to decimals")
# convert budget/revenue fields to numerics - coerce values that do not conform (strings etc)
df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")

LOG.info("Picking values with budget field > 0, so division does not result in infinity")
# choose values with budget greater than 0 to avoid infinity
df = df[df["budget"]>0]

LOG.info("Calculating ratios")
# calculate ratios and round by 5 digits
df["ratio"] = round(df["revenue"]/df["budget"], 5)

LOG.info("Normalizing the production companies field")
df["production_companies"] = df["production_companies"].apply(util.normalize_production_companies)
LOG.info("Normalizing Title")
df["title"] = df["title"].apply(str.lower)

LOG.info("Removing movies with budget < 10000 to filter inaccurate data")
# removing movies with budget < 10000 to filter inaccurate data
df = df[df["budget"]>=10000]

LOG.info("Sorting values by Ratio")
# sort by ratios
df.sort_values("ratio", ascending=False, inplace=True)

LOG.info("Dropping unnecessary columns from movies")
# drop unnecessary columns
df.drop(df.columns.difference(["title", 'budget', "release_date", 'revenue', "rating", "ratio", "production_companies"]), axis=1, inplace=True)
# pick first 1000
df = df.iloc[:1000]
LOG.info("::Movies in dataframe::"+str(len(df)))

LOG.info("::Movies Parsing Complete:: --- %s seconds ---" % (time.time() - start_time))
print("Movies Parsed --- %s seconds ---" % (time.time() - start_time))

