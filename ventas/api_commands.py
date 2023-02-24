from app import app, api, celery, QUEUE_REDIS
import socket
from datetime import datetime
from flask import request
from flask_restful import Resource
import json
import jsonschema
from jsonschema import validate


# Configuracion clase
class VistaOrden(Resource):

    def post(self):
        # Validación de los campos de entrada y enmascaramiento
        orden_validada = {
            "cliente": request.json["cliente"],
            "cliente_id": request.json["cliente_id"],
            "direccion": request.json["direccion"],
            "ciudad": request.json["ciudad"],
            "fecha_pedido": str(datetime.strptime(request.json["fecha_pedido"], '%Y-%m-%d').date()),
            "fecha_entrega": str(datetime.strptime(request.json["fecha_entrega"], '%Y-%m-%d').date()),
            "metodo_pago": request.json["metodo_pago"]
        }

        hostIp = socket.gethostbyname(socket.gethostname())
        orden = self.valida_campos(orden_validada)
        # Envio asyncrono a la cola de redis
        args = (json.dumps(orden),)
        procesar_orden.apply_async(args)
        # Obenemos la ip del servidor que toma la petición
        response = {
            "HTTPCode": 200,
            "IP": hostIp,
        }

        return response

    def valida_campos(self, orden):
        if orden["cliente"] == "":
            orden["cliente"] = "Generico"
        return orden

    def valida_json(self, jsonData):
        try:
            json.loads(jsonData)
        except ValueError as err:
            return False
        return True

    def valida_estructura(self, jsonData):

        ventaSchema = {
            "type": "object",
            "properties": {
                "cliente": {"type": "string"},
                "cliente_id": {"type": "number"},
                "direccion": {"type": "string"},
                "ciudad": {"type": "string"},
                "vendedor": {"type": "string"},
                "fecha_pedido": {"type": "string"},
                "fecha_entrega": {"type": "string"},
                "metodo_pago": {"type": "string"}
            },
        }
        try:
            validate(instance=jsonData, schema=ventaSchema)
        except jsonschema.exceptions.ValidationError as err:
            return False
        return True

# Se configura el metodo para realizar el envio a la cola


@celery.task(name=QUEUE_REDIS)
def procesar_orden(orden_json):
    pass


# Se agregarn los recursos
api.add_resource(VistaOrden, '/cpp/ventas')

# Se inicializa la aplicacion
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
