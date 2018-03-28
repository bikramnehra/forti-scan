import os, requests, json, hashlib, configparser
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import MySQLdb

## Reading config parameters
config = configparser.ConfigParser()
config.read('config.ini')
url = config.get('flask', 'url')
api_key = config.get('flask', 'api_key')
user = config.get('mysql', 'user')
passwd = config.get('mysql', 'passwd')
unix_socket = config.get('mysql', 'unix_socket')
db = config.get('mysql', 'db')
table = config.get('mysql', 'table')
host = config.get('mysql', 'host')

## Setting file upload path to server
UPLOAD_FOLDER = os.getcwd()+'/files/'

## Limiting file upload to only txt files
ALLOWED_EXTENSIONS = set(['txt'])

## App configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn = ''
cursor = ''

## Checking for database connections
try:
	conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, unix_socket=unix_socket)
except:
	print 'Could not connect to the database!!'
else:
	cursor = conn.cursor()

## Setting the base route
@app.route("/")
def index():
    return send_file("templates/index.html")

## Function for filtering only txt files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

## Function for checking if file was already scanned 
def check_database(hash_val):
	data = {}
	## Checking records in database
	if(conn and cursor):
		cursor.execute('SELECT * FROM '+table+' WHERE HASH_VALUE="'+hash_val+'"')
		database_vals = cursor.fetchall()
		if(database_vals):
			data["hashValue"] =  hash_val
			data["fortinetNames"] =  database_vals[0][1]
			if(data["fortinetNames"] == 'None'):
				data["fortinetNames"] = 'null'
			data["numEngines"] = database_vals[0][2]
			data["scanDate"] = database_vals[0][3]
			return data
	## Checking records in database.json file
	else:
		try:
			with open('files/database.json') as data_file:
				database_vals = json.load(data_file)
				if(database_vals):
					vals =  database_vals[hash_val]
					data["hashValue"] = hash_val
					data["fortinetNames"] =  vals["fortinetNames"]
					if(data["fortinetNames"] == 'None'):
						data["fortinetNames"] = 'null'
					data["numEngines"] = vals["numEngines"]
					data["scanDate"] = vals["scanDate"]
		except:
			print 'database.json file could not be opened'
		finally:
			return data


## Function for handling file upload
@app.route("/upload", methods=['POST'])
def upload():
	data = {}
	if request.method == 'POST':
		## Checking if the file exists
		if 'file' not in request.files:
			print 'No file part'
			return redirect(request.url)
        input_file = request.files['file']
        ## Checking if the file is not empty
        if input_file.filename == '':
            print 'No selected file'
            return redirect(request.url)
        ## if file exists and allowed file then do further processing
        if input_file and allowed_file(input_file.filename):
			input_file = request.files['file']
			filename = secure_filename(input_file.filename)
			input_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			## Calculating hash and seeing if it is already scanned
			hash_val = hashlib.md5(open(UPLOAD_FOLDER+filename,'rb').read()).hexdigest()
			database_vals = check_database(hash_val)
			
			## If it is already scanned then retrieve results from database/file
			if(database_vals):
				data = database_vals
				data["isCached"] = 1
			## Otherwise call the API and get results
			else:
				params = {'apikey': api_key}
				files = {'file': (filename, open(UPLOAD_FOLDER+filename, 'rb'))}
				response = requests.post(url, files=files, params=params)
				json_response = response.json()
				
				params = {'apikey': api_key, 'resource': json_response['resource']}
				headers = {"Accept-Encoding": "gzip, deflate", "User-Agent" : "gzip,  My Python requests library example client or username"}
				report_response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
				report_json_response = report_response.json()

				data["hashValue"] =  report_json_response["md5"]
				data["fortinetNames"] =  report_json_response["scans"]["Fortinet"]["result"]
				if(data["fortinetNames"] is None):
					data["fortinetNames"] = 'null'
				data["numEngines"] = len(report_json_response["scans"])
				data["scanDate"] = report_json_response["scan_date"]
				data["isCached"] = 0

				## If database connection is up then insert results in database
				if(conn and cursor):
					insertQuery = "INSERT INTO "+table+" (HASH_VALUE,FORTINET_DETECTION_NAMES,NUMBER_OF_ENGINES_DETECTED,SCAN_DATE) VALUES ('%s','%s','%s','%s')" %(data["hashValue"], data["fortinetNames"], data["numEngines"], data["scanDate"])
					cursor.execute(insertQuery) 
					conn.commit()

				## Otherwise insert results in json file
				else:
					database_data = {
								hash_val: {
		    						"fortinetNames":  data["fortinetNames"],
		    						"numEngines": data["numEngines"],
		    						"scanDate": data["scanDate"]
		    					}
		    		}
					try:
						with open('files/database.json') as f:
							current_data = json.load(f)
						current_data.update(database_data)
						with open('files/database.json', 'w') as outfile:
							json.dump(current_data, outfile)
							
		  			except:
		  				print 'database.json file could not be opened'


	return json.dumps(data)

	
if __name__ == "__main__":
    app.run(host='0.0.0.0')