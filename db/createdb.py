### Script for creating the database

import MySQLdb, configparser, json, os

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('mysql', 'user')
passwd = config.get('mysql', 'passwd')
host = config.get('mysql', 'host')
unix_socket = config.get('mysql', 'unix_socket')
db = config.get('mysql', 'db')
table = config.get('mysql', 'table')

### creating schema and tables  -- one time code
conn = MySQLdb.connect(host=host, user=user, passwd=passwd, unix_socket=unix_socket)
cursor = conn.cursor()
cursor.execute('CREATE DATABASE '+db)
cursor.execute('USE '+db)
cursor.execute('CREATE TABLE '+'`'+db+'`'+'.`'+table+'` (`HASH_VALUE` VARCHAR(256) NOT NULL, `FORTINET_DETECTION_NAMES` VARCHAR(45) NULL, `NUMBER_OF_ENGINES_DETECTED` VARCHAR(45) NULL, `SCAN_DATE` VARCHAR(45) NULL, PRIMARY KEY (`HASH_VALUE`))')

