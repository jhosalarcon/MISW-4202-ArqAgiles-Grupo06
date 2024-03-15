from api import db
from api import ACL
db.create_all()
def add_acl(service, queue):
        acl = ACL(service=service, queue=queue)
        if len(list(ACL.query.filter(ACL.service==service).filter(ACL.queue==queue).all())) == 0:
                db.session.add(acl)
                db.session.commit()

add_acl("sesiones","notification_queue")
add_acl("notificaciones","notification_queue")