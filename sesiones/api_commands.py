from flask import request
from flask_restful import Resource

from base import Persona, Actividad, Sesion, db, sesion_schema, api, app, channel
from notification_sender import enviar_notificacion

class SesionListResource(Resource):
    """Esto clase hace referencia a la interfaz de sesion para iniciar una sesion desde el api gateway"""

    def post(self):
        #user = Persona.query.get(request.json['persona_id'])
        # actividad = Actividad.query.get(request.json['actividad_id'])
        ## if user is None or actividad is None:
        ##    return {'message': 'User or activity not found'}, 400
        new_sesion = Sesion(nombre=request.json['nombre'], fecha=request.json['fecha'],
                            persona_id=request.json['persona_id'], actividad_id=request.json['actividad_id'])

        db.session.add(new_sesion)
        db.session.commit()
        channel.basic_publish(exchange='',
                      routing_key='notification_queue',
                      body=str(new_sesion.id))
        print("Envio de creación de notificacion.")
        return sesion_schema.jsonify(new_sesion)


api.add_resource(SesionListResource, '/api-commands/sesion')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
