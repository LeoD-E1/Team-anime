from flask import Flask
from flask_pymongo import PyMongo
from env import env

app = Flask(__name__)

app.config['MONGO_URI'] = env.get('MONGODB_URI')
mongo = PyMongo(app)

