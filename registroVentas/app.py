from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from celery import Celery
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registro_ventas_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)

# Configuracion Cola
celery = Celery('tasks', broker='redis://redis:6379/0')


@celery.task(name="tabla.orden")
def rigistrar_orden(orden_json):
    json_object = json.loads(orden_json)
    print('Retornando mensaje ===========================================>')
    print(json_object)
    print(f'<== {json_object["cliente"]} ==>')
    print('Fin mensaje ===========================================>')
    registrar_venta_log(json_object)
    

def registrar_venta_log(json_object):
    # Registro de la orden
    with open('log_signin.txt','a') as file:
        file.write(f"{str(json_object)}\n")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
