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
from datetime import timedelta

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

@app.route('/roles', methods=['POST'])
def create_role():
    name = request.json.get("name", None)
    
    role = Role()
    role.name = request.json.get("name", "")
   
    role.save()

    return jsonify({"success": "Register Successfully"}), 200

@app.route('/student_register', methods=['POST'])
def student_register():
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
    student.password = bcrypt.generate_password_hash(password).decode("utf-8")
    student.role_id = "2"

    student.save()

    return jsonify({"success": "Register Successfully"}), 200

@app.route('/staff_register', methods=['POST'])
def staff_register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    staff = StaffUser.query.filter_by(email=email).first()
    if staff:
        return jsonify({"msg": "Email already exists"}), 400
    
    staff = StaffUser()
    staff.name = request.json.get("name", "")
    staff.lastName = request.json.get("lastName", "")
    staff.email = email
    staff.password = bcrypt.generate_password_hash(password).decode("utf-8")
    staff.role_id = "1"

    staff.save()

    return jsonify({"success": "Register Successfully"}), 200

@app.route('/teacher_register', methods=['POST'])
def teacher_register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    teacher = TeacherUser.query.filter_by(email=email).first()
    if teacher:
        return jsonify({"msg": "Email already exists"}), 400
    
    teacher = TeacherUser()
    teacher.name = request.json.get("name", "")
    teacher.lastName = request.json.get("lastName", "")
    teacher.email = email
    teacher.password = bcrypt.generate_password_hash(password).decode("utf-8")
    teacher.role_id = "3"

    teacher.save()

    return jsonify({"success": "Register Successfully"}), 200


@app.route('/student_login', methods=['POST'])
def student_login():
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

    expires = timedelta(days=3)
    
    data = {
        "access_token": create_access_token(identity=student.email, expires_delta=expires),
        "student": student.serialize()
    }
   
    return jsonify({"success": "Log In Successfully", "data": data}), 200

@app.route('/staff_login', methods=['POST'])
def staff_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    staff = StaffUser.query.filter_by(email=email).first()
    if not staff:
        return jsonify({"msg": "Email/password incorrect"}), 400
    
    if not bcrypt.check_password_hash(staff.password, password):
        return jsonify({"msg": "Email/password incorrect"}), 400

    expires = timedelta(days=3)
    
    data = {
        "access_token": create_access_token(identity=staff.email, expires_delta=expires),
        "staff": staff.serialize()
    }
   
    return jsonify({"success": "Log In Successfully", "data": data}), 200


@app.route('/teacher_login', methods=['POST'])
def teacher_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    teacher = TeacherUser.query.filter_by(email=email).first()
    if not teacher:
        return jsonify({"msg": "Email/password incorrect"}), 400
    
    if not bcrypt.check_password_hash(teacher.password, password):
        return jsonify({"msg": "Email/password incorrect"}), 400

    expires = timedelta(days=3)
    
    data = {
        "access_token": create_access_token(identity=teacher.email, expires_delta=expires),
        "teacher": teacher.serialize()
    }
   
    return jsonify({"success": "Log In Successfully", "data": data}), 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
