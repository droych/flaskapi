from flask_mysqldb import MySQL
from src.common.common import app
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2176'
app.config['MYSQL_DB'] = 'flaskauth'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)
