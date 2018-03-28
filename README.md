## Important Note

The application is configured to be run with and without the database. In case database is not configured the scanned data will be persisted in 'files/database.json' file. So if you wan't to try out the app feel free to do so without configuring the database.


## Pre-requisites

Following are the pre-requisites for running the application:

	1. Python: v2.7+
	2. MySQL: vMySQL 5.6.35
	3. MySQLdb python connector specific to OS 

## Installation

Download the repository and install the following modules using pip:

	1. pip install flask
	2. pip install werkzeug
	3. pip install configparser
	4. pip install requests

## Configuration

Replace current configuration parameters with your values in config.ini file:
	
	1. api_key: API key obtained from virusTotal
	2. user: MySQL username
	3. passwd: MySQL password
	4. host: Host where MySQL server is running
	5. unix_socket: path to mysql.sock file
	6. db: name for the database
	7. table: name for the table

## Running

	1. Navigate to project's root directory through the terminal
		cd fortiScan

	2. Create database and table by executing the following script:
		python db/createdb.py

	3. Now run the python flask application using the following command. The above command will start the server at 0.0.0.0:5000:
		python app.py

	4. Navigate to this url and start playing with the app

## Code Layout
.
|-- ./templates
|   `-- ./templates/index.html
|-- ./config.ini
|-- ./app.py
|-- ./db
|   `-- ./db/createdb.py
|-- ./screenshots
|   |-- ./screenshots/Home_Page.png
|   |-- ./screenshots/Report_Page.png
|   `-- ./screenshots/Info.png
|-- ./static
|   |-- ./static/css
|   |   `-- ./static/css/style.css
|   |-- ./static/partials
|   |   |-- ./static/partials/index.html
|   |   `-- ./static/partials/report.html
|   |-- ./static/js
|   |   `-- ./static/js/app.js
|   `-- ./static/img
|       `-- ./static/img/fortinet.png
|-- ./README.md
`-- ./files
    `-- ./files/database.json


## Technology Stack

The application mainly consists of following components:

	1. Angular.js for front-end
	2. Python+Flask for web server
	3. MySQL for data persistence
	4. Built in MacOSX but should be compatible with most Linux variants 

## Issues Encountered

	1. The biggest challenge was to make the app extensible, robust and configurable. It took significant amount of time to architecture the app.
	2. Developing a full stack web app in such a short period of time was challenging
	3. There were integrations issues with the database but eventually resolved them
