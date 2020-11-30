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
from models import db, Role, StaffUser, TeacherUser, StudentUser, Profile, EnrrollmentAgreement, Financing, Payment, Invoice, CreditNote, TeacherQuestionnarie, TeacherQuestion, StudentQuestionnarie, StudentQuestion, TeacherAnswer
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

@app.route('/enrrollment_agreements', methods=['GET'])
@app.route('/enrrollment_agreements/<int:breathecode_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def enrrollment_agreements(breathecode_id = None):
    if request.method == 'GET':
        if breathecode_id is not None:
            agreement = EnrrollmentAgreement.query.filter_by(breathecode_id=breathecode_id).first() # None por defecto si no consigue el registro
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

@app.route('/financing_agreements', methods=['GET', 'POST'])
@app.route('/financing_agreements/<string:rut>', methods=['GET', 'PUT', 'DELETE'])
def financing_agreements(rut = None):
    if request.method == 'GET':
        if rut is not None:
            financing = Financing.query.filter_by(rut=rut).first() # None por defecto si no consigue el registro
            print(rut)
            if financing:
                return jsonify(financing.serialize()), 200
            return jsonify({"msg": "Financing Agreement not found"}), 404
        else:
            financing = Financing.query.all()
            financing = list(map(lambda financing: financing.serialize(), financing))
            return jsonify(financing), 200

    if request.method == 'POST':

        urlPDF = request.json.get("urlPDF", None)
        months = request.json.get("months", None)
        monthlyFee = request.json.get("monthlyFee",None)
        rut = request.json.get("rut", None)
       
        
        if not urlPDF:
            return jsonify({"msg": "URL is required"}), 400
        if not months:
            return jsonify({"msg": "Month is required"}), 400
        if not monthlyFee:
            return jsonify({"msg": "Monthly Fee is required"}), 400
        if not rut:
            return jsonify({"msg": "RUT is required"}), 400
        

        financing = Financing.query.filter_by(rut=rut).first()
        if financing:
            return jsonify({"msg": "Financing Agreement already exists"}), 400
        
        financing = Financing()
        financing.urlPDF = urlPDF
        financing.months = months
        financing.monthlyFee = monthlyFee
        financing.rut = rut

        financing.save()

        return jsonify({"success": "Financing Agreement Register Successfully"}), 200

@app.route('/payments', methods=['GET', 'POST'])
@app.route('/payments/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def payments(id = None):
    if request.method == 'GET':
        if id is not None:
            payment = Payment.query.get(id) # None por defecto si no consigue el registro
            if payment:
                return jsonify(payment.serialize()), 200
            return jsonify({"msg": "Financing Agreement not found"}), 404
        else:
            payment = Payment.query.all()
            payment = list(map(lambda payment: payment.serialize(), payment))
            return jsonify(payment), 200

    if request.method == 'POST':

        urlPDF = request.json.get("urlPDF", None)
        amount = request.json.get("amount",None)
        bank = request.json.get("bank",None)
        payment_method = request.json.get("payment_method",None)
        rut = request.json.get("rut", None)
       
        
        if not urlPDF:
            return jsonify({"msg": "URL is required"}), 400
        if not amount:
            return jsonify({"msg": "Amount is required"}), 400
        if not bank:
            return jsonify({"msg": "Bank is required"}), 400
        if not payment_method:
            return jsonify({"msg": "Payment Method is required"}), 400
        if not rut:
            return jsonify({"msg": "RUT is required"}), 400
        

        payment = Payment.query.filter_by(id=id).first()
        if payment:
            return jsonify({"msg": "Payment already exists"}), 400
        
        payment = Payment()
        payment.urlPDF = urlPDF
        payment.amount = amount
        payment.bank = bank
        payment.payment_method = payment_method
        payment.rut = rut

        payment.save()

        return jsonify({"success": "Payment Register Successfully"}), 200

@app.route('/invoices', methods=['GET', 'POST'])
@app.route('/invoices/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def invoices(id = None):
    if request.method == 'GET':
        if id is not None:
            invoice = Invoice.query.get(id) # None por defecto si no consigue el registro
            if invoice:
                return jsonify(invoice.serialize()), 200
            return jsonify({"msg": "Invoice not found"}), 404
        else:
            invoice = Invoice.query.all()
            invoice = list(map(lambda invoice: invoice.serialize(), invoice))
            return jsonify(invoice), 200

    if request.method == 'POST':

        urlPDF = request.json.get("urlPDF", None)
        date = request.json.get("data", None)
        amount = request.json.get("amount",None)
        rut = request.json.get("rut", None)
       
        
        if not urlPDF:
            return jsonify({"msg": "URL is required"}), 400
        if not date:
            return jsonify({"msg": "Date is required"}), 400
        if not amount:
            return jsonify({"msg": "Amount is required"}), 400
        if not rut:
            return jsonify({"msg": "RUT is required"}), 400
        

        invoice = Invoice.query.filter_by(id=id).first()
        if invoice:
            return jsonify({"msg": "Invoice already exists"}), 400
        
        invoice = Invoice()
        invoice.urlPDF = urlPDF
        invoice.date = date
        invoice.amount = amount
        invoice.rut = rut

        invoice.save()

        return jsonify({"success": "Invoice Register Successfully"}), 200

@app.route('/credit_notes', methods=['GET', 'POST'])
@app.route('/credit_notes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def credit_notes(id = None):
    if request.method == 'GET':
        if id is not None:
            credit_note = CreditNote.query.get(id) # None por defecto si no consigue el registro
            if credit_note:
                return jsonify(credit_note.serialize()), 200
            return jsonify({"msg": "Credit Note not found"}), 404
        else:
            credit_note = CreditNote.query.all()
            credit_note = list(map(lambda credit_note: credit_note.serialize(), credit_note))
            return jsonify(credit_note), 200

    if request.method == 'POST':

        urlPDF = request.json.get("urlPDF", None)
        date = request.json.get("data", None)
        amount = request.json.get("amount",None)
        rut = request.json.get("rut", None)
       
        
        if not urlPDF:
            return jsonify({"msg": "URL is required"}), 400
        if not date:
            return jsonify({"msg": "Date is required"}), 400
        if not amount:
            return jsonify({"msg": "Amount is required"}), 400
        if not rut:
            return jsonify({"msg": "RUT is required"}), 400
        

        credit_note = CreditNote.query.filter_by(id=id).first()
        if credit_note:
            return jsonify({"msg": "Credit Note already exists"}), 400
        
        credit_note = CreditNote()
        credit_note.urlPDF = urlPDF
        credit_note.date = date
        credit_note.amount = amount
        credit_note.rut = rut

        credit_note.save()

        return jsonify({"success": "Credit Note Register Successfully"}), 200        

@app.route('/teacher_questionnaries', methods=['GET', 'POST'])
@app.route('/teacher_questionnaries/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def teacher_questionnaries(id = None):
    if request.method == 'GET':
        if id is not None:
            questionnarie = TeacherQuestionnarie.query.get(id) # None por defecto si no consigue el registro
            if questionnarie:
                return jsonify(questionnarie.serialize()), 200
            return jsonify({"msg": "Questionarie not found"}), 404
        else:
            questionnarie = TeacherQuestionnarie.query.all()
            questionnarie = list(map(lambda questionnarie: questionnarie.serialize(), questionnarie))
            return jsonify(questionnarie), 200

    if request.method == 'POST':

        email = get_jwt_identity()
        staff_user = StaffUser.query.filter_by(email=email).first()

        questionnarie_details = request.json.get("questionnarie_details", None)
        name = request.json.get("name", None)

        if not questionnarie_details:
            return jsonify({"msg": "Questionnarie Detail is required"}), 400
        if not name:
            return jsonify({"msg": "Name is required"}), 400

        questionnarie = TeacherQuestionnarie.query.filter_by(id=id).first()
        if questionnarie:
            return jsonify({"msg": "Questionnarie already exists"}), 400
        
        questionnarie = TeacherQuestionnarie()
        questionnarie.questionnarie_details = questionnarie_details
        questionnarie.name = name
        questionnarie.staff_user = staff_user.id

        questionnarie.save()

        return jsonify({"success": "Questionnarie Register Successfully"}), 200


    if request.method == 'DELETE':

        delete_questionnarie = TeacherQuestionnarie.query.filter_by(id=id).first()
        print(delete_questionnarie)
        db.session.delete(delete_questionnarie)
        db.session.commit()

        return jsonify({"msg": "Questionnarie deleted"}), 200
    
    if request.method == 'PUT':
        update_questionnarie = TeacherQuestionnarie.query.get(id)

        questionnarie_details = request.form.get('questionnarie_details', None)
        name = request.form.get('name', None)

        if questionnarie_details != '':
            update_questionnarie.questionnarie_details = questionnarie_details
        if name != '':
            update_questionnarie.name = name

        db.session.commit()

        return ({'msg': 'Questionnarie Updated'})  


@app.route('/teacher_questions', methods=['GET', 'POST'])
@app.route('/teacher_questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def teacher_question(id = None):
    if request.method == 'GET':
        if id is not None:
            teacher_question = TeacherQuestion.query.get(id) # None por defecto si no consigue el registro
            if teacher_question:
                return jsonify(teacher_question.serialize()), 200
            return jsonify({"msg": "Teacher Question not found"}), 404
        else:
            teacher_question = TeacherQuestion.query.all()
            teacher_question = list(map(lambda teacher_question: teacher_question.serialize(), teacher_question))
            return jsonify(teacher_question), 200

    if request.method == 'POST':

        question = request.json.get("question", None)
       
        if not question:
            return jsonify({"msg": "Question is required"}), 400
        
        teacher_question = TeacherQuestion.query.filter_by(id=id).first()
        if teacher_question:
            return jsonify({"msg": "Question already exists"}), 400
        
        teacher_question = TeacherQuestion()
        teacher_question.question = question
        teacher_question.questionnarie_id = request.json.get("questionnarie_id", None)

        teacher_question.save()

        return jsonify({"success": "Teacher Question Register Successfully"}), 200

    if request.method == 'DELETE':

        delete_question = TeacherQuestion.query.filter_by(id=id).first()
        db.session.delete(delete_question)
        db.session.commit()

        return jsonify({"msg": "Question deleted"}), 200
    
    if request.method == 'PUT':
        update_question = TeacherQuestion.query.get(id)

        question = request.form.get('question', None)
        
        if question != '':
            update_question.question = question
    
        db.session.commit()

        return ({'msg': 'Question Updated'})  


@app.route('/student_questionnaries', methods=['GET', 'POST'])
@app.route('/student_questionnaries/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def student_questionnaries(id = None):
    if request.method == 'GET':
        if id is not None:
            questionnarie = StudentQuestionnarie.query.get(id) # None por defecto si no consigue el registro
            if questionnarie:
                return jsonify(questionnarie.serialize()), 200
            return jsonify({"msg": "Questionarie not found"}), 404
        else:
            questionnarie = StudentQuestionnarie.query.all()
            questionnarie = list(map(lambda questionnarie: questionnarie.serialize(), questionnarie))
            return jsonify(questionnarie), 200

    if request.method == 'POST':

        email = get_jwt_identity()
        staff_user = StaffUser.query.filter_by(email=email).first()

        questionnarie_details = request.json.get("questionnarie_details", None)
        name = request.json.get("name", None)

        if not questionnarie_details:
            return jsonify({"msg": "Questionnarie Detail is required"}), 400
        if not name:
            return jsonify({"msg": "Name is required"}), 400

        questionnarie = StudentQuestionnarie.query.filter_by(id=id).first()
        if questionnarie:
            return jsonify({"msg": "Questionnarie already exists"}), 400
        
        questionnarie = StudentQuestionnarie()
        questionnarie.questionnarie_details = questionnarie_details
        questionnarie.name = name
        questionnarie.staff_user = staff_user.id

        questionnarie.save()

        return jsonify({"success": "Questionnarie Register Successfully"}), 200


    if request.method == 'DELETE':

        delete_questionnarie = StudentQuestionnarie.query.filter_by(id=id).first()
        db.session.delete(delete_questionnarie)
        db.session.commit()

        return jsonify({"msg": "Questionnarie deleted"}), 200
    
    if request.method == 'PUT':
        update_questionnarie = StudentQuestionnarie.query.get(id)

        questionnarie_details = request.form.get('questionnarie_details', None)
        name = request.form.get('name', None)

        if questionnarie_details != '':
            update_questionnarie.questionnarie_details = questionnarie_details
        if name != '':
            update_questionnarie.name = name


        db.session.commit()

        return ({'msg': 'Questionnarie Updated'})  


@app.route('/student_questions', methods=['GET', 'POST'])
@app.route('/student_questions/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def student_questions(id = None):
    if request.method == 'GET':
        if id is not None:
            student_question = StudentQuestion.query.get(id) # None por defecto si no consigue el registro
            if student_question:
                return jsonify(student_question.serialize()), 200
            return jsonify({"msg": "Student Question not found"}), 404
        else:
            student_question = StudentQuestion.query.all()
            student_question = list(map(lambda student_question: student_question.serialize(), student_question))
            return jsonify(student_question), 200

    if request.method == 'POST':

        question = request.json.get("question", None)
       
        if not question:
            return jsonify({"msg": "Question is required"}), 400
        
        student_question = StudentQuestion.query.filter_by(id=id).first()
        if student_question:
            return jsonify({"msg": "Question already exists"}), 400
        
        student_question = StudentQuestion()
        student_question.question = question
        student_question.questionnarie_id = request.json.get("questionnarie_id", None)

        student_question.save()

        return jsonify({"success": "Student Question Register Successfully"}), 200

    if request.method == 'DELETE':

        delete_question = StudentQuestion.query.filter_by(id=id).first()
        db.session.delete(delete_question)
        db.session.commit()

        return jsonify({"msg": "Question deleted"}), 200
    
    if request.method == 'PUT':
        update_question = StudentQuestion.query.get(id)

        question = request.form.get('question', None)
        
        if question != '':
            update_question.question = question
    
        db.session.commit()

        return ({'msg': 'Question Updated'}) 

@app.route('/teacher_answers', methods=['GET', 'POST'])
@app.route('/teacher_answers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def teacher_answer(id = None):
    if request.method == 'GET':
        if id is not None:
            teacher_answer = TeacherAnswer.query.get(id) # None por defecto si no consigue el registro
            if teacher_answer:
                return jsonify(teacher_answer.serialize()), 200
            return jsonify({"msg": "Teacher Answer not found"}), 404
        else:
            teacher_answer = TeacherAnswer.query.all()
            teacher_answer = list(map(lambda teacher_answer: teacher_answer.serialize(), teacher_answer))
            return jsonify(teacher_answer), 200

    if request.method == 'POST':

        answer = request.json.get("answer", None)
       
        if not answer:
            return jsonify({"msg": "Answer is required"}), 400
        
        teacher_answer = TeacherAnswer.query.filter_by(id=id).first()
        if teacher_answer:
            return jsonify({"msg": "Answer already exists"}), 400
        
        teacher_answer = TeacherAnswer()
        teacher_answer.answer = answer
        teacher_answer.questionnarie_id = request.json.get("questionnarie_id", None)

        teacher_answer.save()

        return jsonify({"success": "Teacher Answer Register Successfully"}), 200

    if request.method == 'DELETE':

        delete_answer = TeacherAnswer.query.filter_by(id=id).first()
        db.session.delete(delete_answer)
        db.session.commit()

        return jsonify({"msg": "Answer deleted"}), 200
    
    if request.method == 'PUT':
        update_answer = TeacherAnswer.query.get(id)

        answer = request.form.get('answer', None)
        
        if answer != '':
            update_answer.answer = answer
    
        db.session.commit()

        return ({'msg': 'Answer Updated'})  



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
