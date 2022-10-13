from flask_mysqldb import MySQL
#from src.controller.app import app
from flask import Flask

app = Flask(__name__)
from flask_restful import Api


api = Api(app)
