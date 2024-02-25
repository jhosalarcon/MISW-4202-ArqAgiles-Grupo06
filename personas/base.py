from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
import pika
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'personas.db') ## 'sqlite:////mnt/sesiones.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/personas.db' ## 'sqlite:////mnt/sesiones.db'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    edad = db.Column(db.Integer)



class PersonaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Persona
        load_instance = True

persona_schema = PersonaSchema()
