# TrueLayer

## Pre-requisites

#### Install Python 3.9
	- Go to: https://www.python.org/downloads/release/python-390/
	- Download Python for your Operating System (Windows/Linux)
	- Execute the downloaded file
	- Install Python with default options (ADD PYTHON TO PATH)

#### Install Postgres
	- Go to: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
	- Download postgres for your Operating System (Windows/Linux). 
	- Execute the downloaded file
	- Install the database with default options
	- Remember the password and username for the account you create here, we will need it later on

#### Download this repository from Github through git clone
	- `git clone https://github.com/adnanahmadkhan/TrueLayer.git TrueLayer`

#### From your terminal go into the downloaded repository folder
	- `cd TrueLayer`

#### Go to your bash terminal
	- run the following commands 
	- install virtualenv `pip install virtualenv`
	- create a virtual environment through virtualenv `virtualenv venv`
	- activate that environment 
		- *FOR WINDOWS* `source venv/bin/activate`  
		- *FOR LINUX*  `source venv/Scripts/activate`
		- Successful activation will result in **(venv)** printed on your shell
	- install necessary libraries `pip install -r requirements.txt`


#### Update your env.json file
	- Open env.json file in root of the project repository
	- It will have some default values like data file names, **DO NOT** change them as they are essential to running the script
	- Add/Update the database credentials e.g _dbuser_, _password_, _port_, _dbname_
	- Default _port_ is **5432**, default _dbname_ is **TrueLayer**

#### Download required zipped files and place them in data folder in root of project directory
	- Download https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz
	- Go to https://www.kaggle.com/rounakbanik/the-movies-dataset/version/7#movies_metadata.csv and download the movies_metadata.csv file
	- Place both these files in the data folder in the root of the project directory

#### Run the source code
	- Run the command `python main.py` to run the project