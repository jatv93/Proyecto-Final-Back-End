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
from flask_bcrypt import Bcrypt
from flask_jwt_extended.jwt_manager import JWTManager
from flask_jwt_extended.utils import create_access_token, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from datetime import datetime

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

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

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    student = StudentUser.query.filter_by(email=email).first()
    if student:
        return jsonify({"msg": "Email already exists"}), 400
    
    student = StudentUser()
    student.name = request.json.get("name", "")
    student.lastName = request.json.get("lastName", "")
    student.email = email
    student.password = bcrypt.generate_password_hash(password)
    student.role_id = request.json.get("role_id")

    student.save()

    return jsonify({"success": "Register Successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    student = StudentUser.query.filter_by(email=email).first()
    if not student:
        return jsonify({"msg": "Email/password incorrect"}), 400
    
    if not bcrypt.check_password_hash(student.password, password):
        return jsonify({"msg": "Email/password incorrect"}), 400

    expires = datetime.timedelta(days=3)
    
    data = {
        "access_token": create_access_token(identity=student.email, expires_delta=expires),
        "student": student.serialize()
    }
   
    return jsonify({"success": "Log In Successfully", "data": data}), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
