from flask import request
from flask_restful import Resource
from base import Persona, db, persona_schema, api, app

class PersonaResource(Resource):
    def post(self):
        new_persona = Persona(nombre=request.json['nombre'], edad=request.json['edad'])
        db.session.add(new_persona)
        db.session.commit()
        return persona_schema.dump(new_persona)

api.add_resource(PersonaResource, '/api-commands/personas')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')