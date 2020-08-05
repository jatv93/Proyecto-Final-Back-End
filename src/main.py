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
from models import db, Role, StaffUser, TeacherUser, StudentUser, Profile, EnrrollmentAgreement
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

@app.route('/student_users', methods=['GET','POST'])
@app.route('/student_users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def student_users(id = None):
    if request.method == 'GET':
        if id is not None:
            student = StudentUser.query.get(id) # None por defecto si no consigue el registro
            if student:
                return jsonify(student.serialize()), 200
            return jsonify({"msg": "User not found"}), 404
        else:
            student = StudentUser.query.all()
            student = list(map(lambda student: student.serialize(), student))
            return jsonify(student), 200
    
    if request.method == 'POST':

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
        student.role_id = "1"

        student.save()

        return jsonify({"success": "Register Successfully"}), 200

    if request.method == 'DELETE':

        deleteUser = StudentUser.query.filter_by(id=id).first()
        db.session.delete(deleteUser)
        db.session.commit()
        
        return jsonify({"msg": "User delete successfully"}), 200

@app.route('/staff_users', methods=['GET','POST'])
@app.route('/staff_users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def staff_users(id = None):
    if request.method == 'GET':
        if id is not None:
            staff = StaffUser.query.get(id) # None por defecto si no consigue el registro
            if staff:
                return jsonify(staff.serialize()), 200
            return jsonify({"msg": "User not found"}), 404
        else:
            staff = StaffUser.query.all()
            staff = list(map(lambda staff: staff.serialize(), staff))
            return jsonify(staff), 200
    
    if request.method == 'POST':

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

    if request.method == 'PUT':
        
        editUser = StaffUser.query.get(id)

        name = request.form.get("name", None)
        lastName = request.form.get("lastName", None)    

        if name != '':
            editUser.name = name
        if lastName !='':
            editUser.description = lastName

        db.session.commit()

        return jsonify({"msg": "User Updated"})  

    if request.method == 'DELETE':

        deleteUser = StaffUser.query.filter_by(id=id).first()
        db.session.delete(deleteUser)
        db.session.commit()
        
        return jsonify({"msg": "User delete successfully"}), 200


@app.route('/teacher_users', methods=['GET','POST'])
@app.route('/teacher_users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def teacher_users(id = None):
    if request.method == 'GET':
        if id is not None:
            teacher = TeacherUser.query.get(id) # None por defecto si no consigue el registro
            if teacher:
                return jsonify(teacher.serialize()), 200
            return jsonify({"msg": "User not found"}), 404
        else:
            teacher = TeacherUser.query.all()
            teacher = list(map(lambda teacher: teacher.serialize(), teacher))
            return jsonify(teacher), 200
    
    if request.method == 'POST':

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
        teacher.role_id = "1"

        teacher.save()

        return jsonify({"success": "Register Successfully"}), 200

    if request.method == 'DELETE':

        deleteUser = TeacherUser.query.filter_by(id=id).first()
        db.session.delete(deleteUser)
        db.session.commit()
        
        return jsonify({"msg": "User delete successfully"}), 200

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


@app.route('/profiles', methods=['GET', 'POST'])
@app.route('/profiles/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def profiles(id = None):
    if request.method == 'GET':
        if id is not None:
            profile = Profile.query.get(id) # None por defecto si no consigue el registro
            if profile:
                return jsonify(profile.serialize()), 200
            return jsonify({"msg": "Profile not found"}), 404
        else:
            profile = Profile.query.all()
            profile = list(map(lambda profile: profile.serialize(), profile))
            return jsonify(profile), 200

    if request.method == 'POST':

        student_id = request.json.get("student_id", None)
        breathecode_id = request.json.get("breathecode_id",None)
        address = request.json.get("address", None)
        phone = request.json.get("phone", None)
        size = request.json.get("size", None)
        rut = request.json.get("rut", None)
        cohort = request.json.get("cohort", None)
        name = request.json.get("name", None)
        lastName = request.json.get("lastName", None)
        email = request.json.get("email", None)  


        if not student_id:
            return jsonify({"msg": "Student ID is required"}), 400
        if not breathecode_id:
            return jsonify({"msg": "Breathecode ID is required"}), 400
        if not address:
            return jsonify({"msg": "Address is required"}), 400
        if not phone:
            return jsonify({"msg": "Phone is required"}), 400
        if not size:
            return jsonify({"msg": "Size is required"}), 400
        if not rut:
            return jsonify({"msg": "Rut is required"}), 400
        if not cohort:
            return jsonify({"msg": "Cohort is required"}), 400
        if not name:
            return jsonify({"msg": "Name is required"}), 400
        if not lastName:
            return jsonify({"msg": "Last Name is required"}), 400
        if not email:
            return jsonify({"msg": "Email is required"}), 400

        profile = Profile.query.filter_by(student_id=student_id).first()
        if profile:
            return jsonify({"msg": "Profile already exists"}), 400
        
        profile = Profile()
        profile.student_id = student_id
        profile.breathecode_id = breathecode_id
        profile.address = address
        profile.phone = phone
        profile.size = size
        profile.rut = rut
        profile.cohort = cohort
        profile.name = name
        profile.lastName = lastName
        profile.email = email

        profile.save()

        return jsonify({"success": "Profile Register Successfully"}), 200

@app.route('/enrrollment_agreements', methods=['GET', 'POST'])
@app.route('/enrrollment_agreements/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def enrrollment_agreements(id = None):
    if request.method == 'GET':
        if id is not None:
            agreement = EnrrollmentAgreement.query.get(id) # None por defecto si no consigue el registro
            if agreement:
                return jsonify(agreement.serialize()), 200
            return jsonify({"msg": "Enrrollment Agreement not found"}), 404
        else:
            agreement = EnrrollmentAgreement.query.all()
            agreement = list(map(lambda agreement: agreement.serialize(), agreement))
            return jsonify(agreement), 200

    if request.method == 'POST':

        urlPDF = request.json.get("urlPDF", None)
        breathecode_id = request.json.get("breathecode_id",None)

        if not urlPDF:
            return jsonify({"msg": "URL is required"}), 400
        if not breathecode_id:
            return jsonify({"msg": "Breathecode ID is required"}), 400

        agreement = EnrrollmentAgreement.query.filter_by(breathecode_id=breathecode_id).first()
        if agreement:
            return jsonify({"msg": "Enrrollment Agreement already exists"}), 400
        
        agreement = EnrrollmentAgreement()
        agreement.urlPDF = urlPDF
        agreement.breathecode_id = breathecode_id

        agreement.save()

        return jsonify({"success": "Enrrollment Agreement Register Successfully"}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
