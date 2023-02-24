from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from celery import Celery
from datetime import datetime
import socket

# Configuracion Flask
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()
cors = CORS(app)
api = Api(app)
api.init_app(app)

# Configuracion colas Redis y Celery
QUEUE_REDIS = "tabla.orden"
celery = Celery('tasks', broker='redis://redis:6379/0')