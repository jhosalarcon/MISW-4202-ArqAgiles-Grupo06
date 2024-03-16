from flask import request
from flask_restful import Resource
from base import Actividad, db, actividad_schema, api, app

class ActividadResource(Resource):
    def post(self):
        new_actividad = Actividad(nombre=request.json['nombre'], descripcion=request.json['descripcion'], duracion=request.json['duracion'])
        db.session.add(new_actividad)
        db.session.commit()
        return actividad_schema.dump(new_actividad)

api.add_resource(ActividadResource, '/api-commands/actividades')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')