from flask import request
import requests
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from base import Sesion, db, sesion_schema, api, app, channel #Persona

class SesionListResource(Resource):
    """Esto clase hace referencia a la interfaz de sesion para iniciar una sesion desde el api gateway"""
    @jwt_required()
    def post(self):
        has_acccess_request = requests.get(f"http://acl-queries:5000/api-queries/acl/sesiones/notification_queue",headers=request.headers)
        if has_acccess_request.status_code == 403:
             return {'message': 'Acceso denegado'}, 403
        if has_acccess_request.status_code == 401:
             return {'message': 'Token invalido'}, 401

        persona_response = requests.get(f"http://personas-queries:5000/api-queries/personas/{request.json['persona_id']}")
        actividad_response = requests.get(f"http://actividades-queries:5000/api-queries/actividades/{request.json['actividad_id']}")
        if persona_response.status_code == 404 or actividad_response.status_code == 404:
            return {'message': 'User or activity not found'}, 400
        new_sesion = Sesion(nombre=request.json['nombre'], fecha=request.json['fecha'],
                            persona_id=request.json['persona_id'], actividad_id=request.json['actividad_id'])

        db.session.add(new_sesion)
        db.session.commit()

        # actividad_duration = int(actividad_response.json()['duracion'])

        #actividad_duration = 10
        #def publish_message_every_2_seconds(args, channel):
        #    start = 0
        #    print('AAAAA', flush=True)
        #    print(args, flush=True)
        #    while actividad_duration -start > 0:
        #        channel.basic_publish(exchange='',
        #                              routing_key='notification_queue',
        #                              body=str(args))
        #        print("Message published.")
        #        time.sleep(2)
        #        start += 2

        # threading.Thread(target=publish_message_every_2_seconds, args=(new_sesion.id,channel)).start()

        channel.basic_publish(exchange='',
                      routing_key='notification_queue',
                      body=str(new_sesion.id))
        print("Envio de creación de notificacion.")
        return sesion_schema.jsonify(new_sesion)


api.add_resource(SesionListResource, '/api-commands/sesion')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
