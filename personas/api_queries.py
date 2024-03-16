from base import persona_schema, Persona, api, app
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class PersonaResource(Resource):
    @jwt_required()
    def get(self, persona_id):
        persona = Persona.query.get_or_404(persona_id)
        return persona_schema.dump(persona)


api.add_resource(PersonaResource, '/api-queries/personas/<int:persona_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')