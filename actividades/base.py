from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager
import pika
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'personas.db') ## 'sqlite:////mnt/sesiones.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/actividades.db' ## 'sqlite:////mnt/sesiones.db'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = True

jwt = JWTManager(app)
ma = Marshmallow(app)
api = Api(app)


class Actividad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(100))
    duracion = db.Column(db.Integer)



class ActividadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Actividad
        load_instance = True

actividad_schema = ActividadSchema()
