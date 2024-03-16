import datetime
import time
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-jwt"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
jwt = JWTManager(app)
api = Api(app)

class AuthResource(Resource):
    def get(self, persona_id):
        access_token = create_access_token(identity=persona_id, expires_delta=datetime.timedelta(minutes=2))
        return jsonify(access_token=access_token)

api.add_resource(AuthResource, '/api-queries/jwt/<int:persona_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')