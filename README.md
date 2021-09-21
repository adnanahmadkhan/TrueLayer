# TrueLayer

## Pre-requisites

#### Install Python 3.9
1. Go to: https://www.python.org/downloads/release/python-390/
2. Download Python for your Operating System (Windows/Linux)
3. Execute the downloaded file
4. Install Python with default options (ADD PYTHON TO PATH)

#### Install Postgres
1. Go to: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
2. Download postgres for your Operating System (Windows/Linux). 
3. Execute the downloaded file
4. Install the database with default options
5. Remember the password and username(usually _postgres_) for the account you create here, we will need it later on


#### Download this repository from Github through git clone
1. `git clone https://github.com/adnanahmadkhan/TrueLayer.git TrueLayer`


#### From your terminal go into the downloaded repository folder
1. `cd TrueLayer`


#### Go to your terminal
1. run the following commands 
2. install virtualenv `pip install virtualenv`
3. create a virtual environment through virtualenv `virtualenv venv`
4. activate that environment 
	4.1 *FOR WINDOWS* `source venv/bin/activate`  
	4.2 *FOR LINUX*  `source venv/Scripts/activate`
	4.3 Successful activation will result in **(venv)** printed on your shell
5. install necessary libraries `pip install -r requirements.txt`


#### Update your env.json file
1. Open env.json file in root of the project repository
2. It will have some default values like data file names, **DO NOT** change them as they are essential to running the script
3. Add/Update the database credentials e.g _dbuser_, _password_, _port_, _dbname_
4. Default _port_ is **5432**, default _dbname_ is **TrueLayer**


#### Download required zipped files and place them in data folder in root of project directory
1. Download https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
2. Go to https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv and download the _movies_metadata.csv_ file
3. Place both these files in the *_data_* folder in the root of the project directory


#### Run the source code
1. Run the command `python main.py` to run the project




## Querying the data
1. When we install postgres, pgadmin 4 is installed by default. We can use this tool to query our data after our script is done running. 
2. From the start menu open pgAdmin 4. Enter your username/password and connect to the TrueLayer database. Open the query editor. Some queries to run are as follows.
3. `SELECT COUNT(*) FROM final;` to count the total number of entries in our database
4. `SELECT title, release_date, ratio, budget, revenue FROM final order by ratio DESC;` to see the movies in order of the budget/revenue ratio. Omitting fields for brevity.
5. `SELECT COUNT(*) from final where ratio > 10;` to see how many movies that made more than 10 folds their investment.
6. `SELECT * from final where LOWER(production_companies) like '%walt disney%';` to see the movies made by some specific producer e.g Walt Disney
7. `SELECT COUNT(*) from final where LOWER(production_companies) like '%walt disney%';` to see how many movies made by some specific producer e.g Walt Disney
8. `SELECT count(_id) as movies, date_part('year', release_date) as release_year from final group by release_year order by movies DESC;` to see the frequency of movies by release date


## Tool Choice
1. Python: Because of the array of tools python provides for processing large scale data. Some of these are given below.
	1. xml elementtree: This is one of the fastest xml parsing library there is. The implementation in the backend is using C. It is extremely simple to use.
	2. pandas dataframe: This is hands down the most powerful & fast big data handling/processing data structure out there. Less code, more work done.
	3. psycopg2: For handling connections to the postgres database. I used the database driver because there was nothing that it can't do that an ORM can. It also has the perk of being faster than ORMs like SQL Alchemy.
	4. virtual environments: To handle dependency management.


## Algorithmic choices
1. While parsing the large XML file, I chose to go over each element at a time and not keep the whole tree in memory by flushing elements I had already gone over. This allowed me to stream the large file, pick/filter objects of interest.
2. I decided to go for in memory processing rather than saving the wikipedia data in a database and then matching/merging it with the movies data. Although the later was my initial approach, when I saw that the filtered file with the fields I needed to merge with the movies file was small enough to keep and process in memory there was no going back. The initial approach was much slower than this one.
3. To match the title in Wikipedia with the movies dataset I used a 6 phased approach.
	1. To give an example if **avatar 2: amazing movie** is the _title_ and **2017-09-01** is the _release_date_ in the movies csv file and I need to search it in the Wikipedia dictionary I made from the XML file I would search for titles in the following order.
	2. avatar 2: amazing movie (2017 film)
	3. avatar 2: amazing movie (film)
	4. avatar 2: amazing movie
	5. avatar 2 (2017 film)
	6. avatar 2 (film)
	7. avatar 2
	8. This is because the wikipedia naming convention for movies in case of ambiguitaion adds the release year/film to remove ambiguition between different topics. 
	9. For titles that were not found after these 6 approaches, those records were added with the Wikipedia fields as empty. 
	10. As such there were 42/1000 records like this. This was found using this query `select * from final where coalesce(url, '') = '';`



