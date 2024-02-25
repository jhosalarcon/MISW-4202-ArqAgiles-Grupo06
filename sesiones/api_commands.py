import threading
import time

from flask import request
import requests
from flask_restful import Resource

from base import Sesion, db, sesion_schema, api, app, channel, Actividad #Persona

class SesionListResource(Resource):
    """Esto clase hace referencia a la interfaz de sesion para iniciar una sesion desde el api gateway"""

    def post(self):
        persona_response = requests.get(f"http://personas-queries:5000/api-queries/personas/{request.json['persona_id']}")
        actividad_response = requests.get(f"http://personas-queries:5000/api-queries/actividades/{request.json['actividad_id']}")
        if persona_response.status_code != 404 or actividad_response.status_code != 404:
            return {'message': 'User or activity not found'}, 400
        new_sesion = Sesion(nombre=request.json['nombre'], fecha=request.json['fecha'],
                            persona_id=request.json['persona_id'], actividad_id=request.json['actividad_id'])

        db.session.add(new_sesion)
        db.session.commit()

        actividad_duration = actividad_response.json()['duration']

        def publish_message_every_2_seconds():
            start = 0
            while actividad_duration -start > 0:
                channel.basic_publish(exchange='',
                                      routing_key='notification_queue',
                                      body=str(new_sesion.id))
                print("Message published.")
                time.sleep(2)
                start += 2

        threading.Thread(target=publish_message_every_2_seconds).start()

        channel.basic_publish(exchange='',
                      routing_key='notification_queue',
                      body=str(new_sesion.id))
        print("Envio de creación de notificacion.")
        return sesion_schema.jsonify(new_sesion)


api.add_resource(SesionListResource, '/api-commands/sesion')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
