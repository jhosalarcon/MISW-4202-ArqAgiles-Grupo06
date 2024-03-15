from http.client import NOT_FOUND
from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/acl.db'
app_context = app.app_context()
app_context.push()
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = True

jwt = JWTManager(app)
api = Api(app)

class ACL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String(50))
    queue = db.Column(db.String(50))

class ACLSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id",)

ACL_schema = ACLSchema()

class ACLResource(Resource):
    @jwt_required()
    def get(self, service_name, queue_name):
        acl = ACL.query.filter(ACL.service==service_name).filter(ACL.queue==queue_name).first()
        if acl is None:
            return {'message': 'Accesso denegado'}, 403
        return ACL_schema.dump(acl)

api.add_resource(ACLResource, '/api-queries/acl/<string:service_name>/<string:queue_name>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') ##, ssl_context='adhoc')