import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import pika

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'notificaciones.db') ## 'sqlite:////mnt/sesiones.db' 
app_context = app.app_context() 
app_context.push()
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Notificacion(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        sesion_id = db.Column(db.String(100))

class NotificacionSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            fields = ('id', 'sesion_id')

notificacion_schema = NotificacionSchema()

amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(url_params)
channel = connection.channel()
channel.queue_declare(queue='notification_queue')


    




