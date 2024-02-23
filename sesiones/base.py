from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from notification_sender import enviar_notificacion
import pika
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sesiones.db') ## 'sqlite:////mnt/sesiones.db' 
app_context = app.app_context() 
app_context.push()
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

# read rabbitmq connection url from environment variable
amqp_url = os.environ['AMQP_URL']
url_params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(url_params)
channel = connection.channel()
channel.queue_declare(queue='notification_queue')

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    edad = db.Column(db.Integer)


class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    duracion = db.Column(db.Integer)


class Sesion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    fecha = db.Column(db.String(100))
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))
    actividad_id = db.Column(db.Integer, db.ForeignKey('actividad.id'))


class SesionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nombre', 'fecha', 'persona_id', 'actividad_id')


sesion_schema = SesionSchema()
