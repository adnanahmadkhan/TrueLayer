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
5. Remember the password and username for the account you create here, we will need it later on

#### Download this repository from Github through git clone
1. `git clone https://github.com/adnanahmadkhan/TrueLayer.git TrueLayer`

#### From your terminal go into the downloaded repository folder
1. `cd TrueLayer`

#### Go to your bash terminal
1. run the following commands 
2. install virtualenv `pip install virtualenv`
3. create a virtual environment through virtualenv `virtualenv venv`
4. activate that environment 
	*FOR WINDOWS* `source venv/bin/activate`  
	*FOR LINUX*  `source venv/Scripts/activate`
	Successful activation will result in **(venv)** printed on your shell
5. install necessary libraries `pip install -r requirements.txt`


#### Update your env.json file
1. Open env.json file in root of the project repository
2. It will have some default values like data file names, **DO NOT** change them as they are essential to running the script
3. Add/Update the database credentials e.g _dbuser_, _password_, _port_, _dbname_
4. Default _port_ is **5432**, default _dbname_ is **TrueLayer**

#### Download required zipped files and place them in data folder in root of project directory
1. Download https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
2. Go to https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv and download the movies_metadata.csv file
3. Place both these files in the data folder in the root of the project directory

#### Run the source code
1. Run the command `python main.py` to run the project
