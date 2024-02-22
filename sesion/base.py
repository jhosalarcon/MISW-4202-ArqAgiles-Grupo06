from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from redis import Redis
from rq import Queue
from notification_sender import enviar_notificacion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sesion.db'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
q = Queue(connection=Redis(host='localhost', port=6379, db=0))


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


def enviar_notificacion_de_actividad(id_sesion):
    sesion = Sesion.query.get(id_sesion)
    persona = Persona.query.get(sesion.persona_id)
    actividad = Actividad.query.get(sesion.actividad_id)

    q.enqueue(enviar_notificacion, {'nombre': persona.nombre, 'actividad': actividad.nombre, 'fecha': sesion.fecha})
