from flask import request
from flask_restful import Resource


from base import Notificacion, db, notificacion_schema, api, app, channel ##q

class NotificacionResource(Resource):
    """Esto clase hace referencia a la interfaz de sesion para iniciar una sesion desde el api gateway"""
    def post(self):
        notificacion = Notificacion.query.filter_by(sesion_id=request.json['sesion_id']).first()
        if notificacion is not None:
            return {'message': 'Ya existe una sesion activa'}, 400
        new_notification = Notificacion(sesion_id=request.json['sesion_id'])
        db.session.add(new_notification)
        db.session.commit()
        channel.basic_publish(exchange='',
                      routing_key='session_queue',
                      body=str(new_notification.id))
        print(" Notificacion enviada desde commandos....!!'")
        return notificacion_schema.dump(new_notification)

api.add_resource(NotificacionResource, '/api-commands/notificaciones')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')