import pandas as pd
from utils import util

movies_file = "./data/movies_metadata.csv.zip"

# read csv file
df = pd.read_csv(movies_file, engine="c")

# convert budget/revenue fields to numerics - coerce values that do not conform (strings etc)
df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["popularity"] = pd.to_numeric(df["popularity"], errors="coerce")

# choose values with budget greater than 0 to avoid infinity
df = df[df["budget"]>0]
# calculate ratios and round by 5 digits
df["ratio"] = round(df["revenue"]/df["budget"], 5)

df["production_companies"] = df["production_companies"].apply(util.normalize_production_companies)
df["title"] = df["title"].apply(str.lower)
# removing movies with budget < 10000 to filter inaccurate data
df = df[df["budget"]>=10000]

# sort by ratios
df.sort_values("ratio", ascending=False, inplace=True)

df.drop(df.columns.difference(["title", 'budget', "release_date", 'revenue', "rating", "ratio", "production_companies"]), axis=1, inplace=True)
# pick first 1000
df = df.iloc[:1000]

# # sort by release date and show first 1000
# df.release_date = pd.to_datetime(df.release_date)
# df.sort_values("release_date", ascending=False, inplace=True)
# print(df.head(1000))

# # sort by revenue and show first 1000
# df.sort_values("revenue", ascending=False, inplace=True)
# print(df.head(1000))




