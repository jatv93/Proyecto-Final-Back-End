from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from datetime import datetime

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    staffusers = db.relationship('StaffUser', backref='role', lazy=True)
    teacherusers = db.relationship('TeacherUser', backref='role', lazy=True)
    studentusers = db.relationship('StudentUser', backref='role', lazy=True)

    def __repr__(self):
        return f"role('{self.name}'"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            # do not serialize the password, its a security breach
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StaffUser(db.Model):
    __tablename__ = 'staff_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, default="")
    lastName = db.Column(db.String(120), unique=False, default="")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"staffUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            "role": self.role.serialize()

            # do not serialize the password, its a security breach
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TeacherUser(db.Model):
    __tablename__ = 'teacher_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, default="")
    lastName = db.Column(db.String(120), unique=False, default="")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"teacherUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            "role": self.role.serialize()
            
            # do not serialize the password, its a security breach
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentUser(db.Model):
    __tablename__ = 'student_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, default="")
    lastName = db.Column(db.String(120), unique=False, default="")
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    profiles = db.relationship('Profile', backref='studentUser', lazy=True)

    def __repr__(self):
        return f"studentUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            "role": self.role.serialize()
            
            # do not serialize the password, its a security breach
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_users.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.String(100), unique=True, nullable=False)
    size = db.Column(db.String(20), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)
    cohort = db.Column(db.String(80), unique=False, nullable=False)
    rut = db.Column(db.String(100), unique=True, nullable=False)
    enrrollment_agreement = db.relationship("EnrrollmentAgreement", backref="agreement", uselist=False)
    financing_agreement = db.relationship("Financing", backref="financing", uselist=False)
    credit_notes = db.relationship('CreditNote', backref='credit_note', lazy=True)
    payments = db.relationship('Payment', backref='payments', lazy=True)
    invoices = db.relationship('Invoice', backref='invoices', lazy=True)

    def __repr__(self):
        return f"profile('{self.breathecodeID}', '{self.size}', '{self.address}','{self.phone}', '{self.cohort}', '{self.rut}')"

    def serialize(self):
        return {
            "id": self.id,
            "breathecodeID": self.breathecodeID,
            "size": self.size,
            "address": self.address,
            "phone": self.phone,
            "cohort": self.cohort,
            "rut": self.rut,
            "enrrollment_agreement": self.agreement.serialize
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class EnrrollmentAgreement(db.Model):
    __tablename__ = 'enrrollment_agreements'
    id = db.Column(db.Integer, primary_key=True)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)


    def __repr__(self):
        return f"agreement('{self.urlPDF}', '{self.breathecodeID}')"


    def serialize(self):
        return {
            "id": self.id,
            "urlPDF": self.urlPDF,
            "breathecodeID": self.breathecodeID
          
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Financing(db.Model):
    __tablename__ = 'financing_agreements'
    id = db.Column(db.Integer, primary_key=True)
    months = db.Column(db.String(100), unique=False, nullable=False)
    monthlyFee = db.Column(db.String(100), unique=False, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    rut = db.Column(db.Integer, db.ForeignKey('profiles.rut'), unique=True, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return f"financing('{self.months}', '{self.monthlyFee}', '{self.date}','{self.rut}', '{self.urlPDF}')"


    def serialize(self):
        return {
            "id": self.id,
            "months": self.months,
            "monthlyFee": self.monthlyFee,
            "urlPDF": self.urlPDF,
            "rut": self.rut

        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.String(100), unique=False, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    payment_method = db.Column(db.String(200), unique=False, nullable=False)
    bank = db.Column(db.String(200), unique=False, nullable=False)
    rut = db.Column(db.Integer, db.ForeignKey('profiles.rut'), unique=True, nullable=False)


    def __repr__(self):
        return f"payment('{self.date}', '{self.amount}', '{self.urlPDF}','{self.payment_method}', '{self.bank}', '{self.rut}')"


    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "urlPDF": self.urlPDF,
            "payment_method": self.payment_method,
            "bank": self.bank,
            "rut": self.rut

        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.String(100), unique=False, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    rut = db.Column(db.Integer, db.ForeignKey('profiles.rut'), unique=True, nullable=False)


    def __repr__(self):
        return f"payment('{self.date}', '{self.amount}', '{self.urlPDF}','{self.rut}')"

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "urlPDF": self.urlPDF,
            "rut": self.rut

        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class CreditNote(db.Model):
    __tablename__ = 'credit_notes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.String(100), unique=False, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    rut = db.Column(db.String, db.ForeignKey('profiles.rut'), unique=True, nullable=False)


    def __repr__(self):
        return f"payment('{self.date}', '{self.amount}', '{self.urlPDF}', '{self.rut}')"

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "urlPDF": self.urlPDF,
            "rut": self.rut
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class JobProfile(db.Model):
    __tablename__ = 'job_profiles'
    id = db.Column(db.Integer, primary_key=True)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    
    def __repr__(self):
        return f"payment('{self.breathecodeID}', '{self.urlPDF}')"

    def serialize(self):
        return {
            "id": self.id,
            "breathecodeID": self.breathecodeID,
            "urlPDF": self.urlPDF       
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Rut(db.Model):
    __tablename__ = 'ruts'
    id = db.Column(db.Integer, primary_key=True)
    rut_id = db.Column(db.Integer, db.ForeignKey('profiles.rut'), unique=True, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    
    def __repr__(self):
        return f"rut('{self.rut_id}', '{self.urlPDF}')"

    def serialize(self):
        return {
            "id": self.id,
            "rut_id": self.rut_id,
            "urlPDF": self.urlPDF       
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TeacherQuestionnarie(db.Model):
    __tablename__ = 'teacher_questionnaries'
    id = db.Column(db.Integer, primary_key=True)
    staff_user = db.Column(db.Integer, db.ForeignKey('staff_users.id'), unique=True, nullable=False)
    questionnarie_details = db.Column(db.String(200), unique=False, nullable=False)
    strenght_question = db.relationship('StrenghtQuestion', backref='strenght', lazy=True)
    weakness_question = db.relationship('WeaknessQuestion', backref='weakness', lazy=True)
    projection_question = db.relationship('ProjectionQuestion', backref='projection', lazy=True)

    def __repr__(self):
        return f"teacher_questionnaries('{self.staff_id}', '{self.questionnarie_details}', '{self.strenght_question}' , '{self.weakness_question}', '{self.projection_question}')"

    def serialize(self):
        return {
            "id": self.id,
            "staff_id": self.staffUser.serialize,
            "questionnarie_details": self.questionnarie_details,
            "strenght_question": self.strenght.serialize,
            "weakness_question": self.weakness.serialize,
            "projection_question": self.projection.serialize
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StrenghtQuestion(db.Model):
    __tablename__ = 'strength_questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    question = db.Column(db.String(200), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f"strength_questions('{self.questionnarie_id}', '{self.question}', '{self.status}')"

    def serialize(self):

        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "question": self.question,
            "status": self.status
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class WeaknessQuestion(db.Model):
    __tablename__ = 'weakness_questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    question = db.Column(db.String(200), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f"weakness_questions('{self.questionnarie_id}', '{self.question}', '{self.status}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "question": self.question,
            "status": self.status
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ProjectionQuestion(db.Model):
    __tablename__ = 'projection_questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    question = db.Column(db.String(200), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f"projection_questions('{self.questionnarie_id}', '{self.question}', '{self.status}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "question": self.question,
            "status": self.status
            
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TeacherStrengthAnswer(db.Model):
    __tablename__ = 'teacher_strength_answers'
    id = db.Column(db.Integer, primary_key=True)
    strenghtQuestion_id = db.Column(db.Integer, db.ForeignKey('strength_questions.id'), unique=True, nullable=False)
    answer = db.Column(db.String(200), unique=False, nullable=False)
    teacher_user = db.Column(db.Integer, db.ForeignKey('teacher_users.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    
    def __repr__(self):
        return f"teacher_answers('{self.strenghtQuestion_id}', '{self.projectionQuestion_id}', '{self.answer}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "answer": self.answer,
            "teacher_user": self.teacher_user,
            "breathecodeID": self.breathecodeID,
            "date": self.date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TeacherWeaknessAnswer(db.Model):
    __tablename__ = 'teacher_weakness_answers'
    id = db.Column(db.Integer, primary_key=True)
    weaknessQuestion_id = db.Column(db.Integer, db.ForeignKey('weakness_questions.id'), unique=True, nullable=False)
    answer = db.Column(db.String(200), unique=False, nullable=False)
    teacher_user = db.Column(db.Integer, db.ForeignKey('teacher_users.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    
    def __repr__(self):
        return f"teacher_answers( '{self.weaknessQuestion_id}','{self.answer}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "answer": self.answer,
            "teacher_user": self.teacher_user,
            "breathecodeID": self.breathecodeID,
            "date": self.date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class TeacherProjectionAnswer(db.Model):
    __tablename__ = 'teacher_projection_answers'
    id = db.Column(db.Integer, primary_key=True)
    projectionQuestion_id = db.Column(db.Integer, db.ForeignKey('projection_questions.id'), unique=True, nullable=False)
    answer = db.Column(db.String(200), unique=False, nullable=False)
    teacher_user = db.Column(db.Integer, db.ForeignKey('teacher_users.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('teacher_questionnaries.id'), unique=True, nullable=False)
    
    def __repr__(self):
        return f"teacher_answers('{self.projectionQuestion_id}', '{self.answer}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "answer": self.answer,
            "teacher_user": self.teacher_user,
            "breathecodeID": self.breathecodeID,
            "date": self.date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentQuestionnarie(db.Model):
    __tablename__ = 'student_questionnaries'
    id = db.Column(db.Integer, primary_key=True)
    staff_user = db.Column(db.Integer, db.ForeignKey('staff_users.id'), unique=True, nullable=False)
    questionnarie_details = db.Column(db.String(200), unique=False, nullable=False)
       
    
    def __repr__(self):
        return f"student_questionnaries('{self.staff_user}', '{self.questionnarie_details}')"

    def serialize(self):
        return {
            "id": self.id,
            "staff_user": self.staff_user,
            "questionnarie_details": self.questionnarie_details
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentQuestion(db.Model):
    __tablename__ = 'student_questions'
    id = db.Column(db.Integer, primary_key=True)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('student_questionnaries.id'), unique=True, nullable=False)
    question = db.Column(db.String(200), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    breathecodeID = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return f"student_questions('{self.questionnarie_id}', '{self.question}' , '{self.status}', '{self.breathecode_id}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "question": self.question,
            "status": self.status,
            "breathecode_id": self.breathecodeID
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class StudentAnswer(db.Model):
    __tablename__ = 'student_answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('student_questions.id'), unique=True, nullable=False)
    answer = db.Column(db.String(200), unique=False, nullable=False)
    teacher_user = db.Column(db.Integer, db.ForeignKey('teacher_users.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.Integer, db.ForeignKey('profiles.breathecodeID'), unique=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    questionnarie_id = db.Column(db.Integer, db.ForeignKey('student_questionnaries.id'), unique=True, nullable=False)
    
    def __repr__(self):
        return f"student_answers('{self.question_id}', '{self.answer}')"

    def serialize(self):
        return {
            "id": self.id,
            "questionnarie_id": self.questionnarie_id,
            "answer": self.answer,
            "teacher_user": self.teacher_user,
            "breathecodeID": self.breathecodeID,
            "date": self.date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()