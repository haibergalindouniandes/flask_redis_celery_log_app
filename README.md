# flask_redis_celery_log_app
Aplicacion que permite registrar en un log las transacciones que son enviadas a la cola de Redis desde Celery

Aplicación FLASK - PYTHON
Redis -> Como broker de mensajes
Celery -> Para el envio asincrono de mensajes
Docker -> Para la contenerizacion de los proyectos:
    -> ventas -> Proyecto que recibe un request y lo envio a la cola de Redis a traves de Celery
    -> registroVentas -> Proyecto que a traves de un worker de Celery toma el mensaje de la cola Redis y escribe un log
NGINX -> API Gateway que permite realizar el balanceo de cargas de los proyectos ventas

