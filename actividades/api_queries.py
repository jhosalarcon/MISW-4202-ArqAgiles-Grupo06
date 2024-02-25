from base import actividad_schema, Actividad, api, app
from flask_restful import Resource

class ActividadResource(Resource):
    def get(self, actividad_id):
        actividad = Actividad.query.get_or_404(actividad_id)
        return actividad_schema.dump(actividad)


api.add_resource(ActividadResource, '/api-queries/actividades/<int:actividad_id>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')