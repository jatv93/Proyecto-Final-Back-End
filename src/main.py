"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Role, StaffUser, TeacherUser, StudentUser, Profile


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/roles', methods=['GET'])
def roles():

    response_body = {
        "msg": "Hello, this is your GET /role response "
    }

    return jsonify(response_body), 200

@app.route('/staff_users/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def staff_users(id = None):

    if request.method == 'GET':
        if id is not None:
            staff = staff_users.query.get(id) # None por defecto si no consigue el registro
            if staff:
                return jsonify(staff.serialize()), 200
            return jsonify({"msg": "Test not found"}), 404

    response_body = {
        "msg": "Hello, this is your GET /staff response "
    }

    return jsonify(response_body), 200

@app.route('/teacher_users', methods=['GET'])
def teacher_users():

    response_body = {
        "msg": "Hello, this is your GET /teacher response "
    }

    return jsonify(response_body), 200

@app.route('/student_users', methods=['GET'])
def student_users():

    response_body = {
        "msg": "Hello, this is your GET /student response "
    }

    return jsonify(response_body), 200










# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
