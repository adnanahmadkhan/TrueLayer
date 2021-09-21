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
1. When we install postgres, pgadmin 4 is installed by default. We can use this tool to query our data after our script is done running. Some queries are as follows.
2. `SELECT COUNT(*) FROM final;` to count the total number of entries in our database
3. `SELECT title, release_date, ratio, budget, revenue FROM final order by ratio DESC;` to see the movies in order of the budget/revenue ratio. Omitting fields for brevity.
4. `SELECT COUNT(*) from final where ratio > 10;` to see how many movies that made more than 10 folds their investment.
5.  `SELECT * from final where LOWER(production_companies) like '%walt disney%';` to see the movies made by some specific producer e.g Walt Disney
6.  `SELECT COUNT(*) from final where LOWER(production_companies) like '%walt disney%';` to see how many movies made by some specific producer e.g Walt Disney
7.  `SELECT count(_id) as movies, date_part('year', release_date) as release_year from final group by release_year order by movies DESC;` to see the frequency of movies by release date
