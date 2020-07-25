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

class StaffUser(db.Model):
    __tablename__ = 'staffUsers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"staffUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,

            # do not serialize the password, its a security breach
        }


class TeacherUser(db.Model):
    __tablename__ = 'teacherUsers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"teacherUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            
            # do not serialize the password, its a security breach
        }

class StudentUser(db.Model):
    __tablename__ = 'studentUsers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    lastName = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    profiles = db.relationship('Profile', backref='studentUser', lazy=True)

    def __repr__(self):
        return f"studentUser('{self.name}', '{self.lastName}', '{self.email}','{self.password}')"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastName": self.lastName,
            "email": self.email,
            
            # do not serialize the password, its a security breach
        }

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('studentUsers.id'), unique=True, nullable=False)
    breathecodeID = db.Column(db.String(100), unique=True, nullable=False)
    size = db.Column(db.String(20), unique=False, nullable=False)
    address = db.Column(db.String(200), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)
    cohort = db.Column(db.String(80), unique=False, nullable=False)
    rut = db.Column(db.String(100), unique=True, nullable=False)
    enrrollment_agreement = db.relationship("EnrrollmentAgreement", backref="profile", uselist=False)
    financing_agreement = db.relationship("Financing", backref="profile", uselist=False)
    credit_notes = db.relationship('CreditNote', backref='profile', lazy=True)
    payments = db.relationship('Payment', backref='profile', lazy=True)
    invoices = db.relationship('Invoice', backref='profile', lazy=True)

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
            "rut": self.rut 
            
        }

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

class CreditNote(db.Model):
    __tablename__ = 'credit_notes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.String(100), unique=False, nullable=False)
    urlPDF = db.Column(db.String(200), unique=False, nullable=False)
    rut = db.Column(db.Integer, db.ForeignKey('profiles.rut'), unique=True, nullable=False)


    def __repr__(self):
        return f"payment('{self.date}', '{self.amount}', '{self.urlPDF}', '{self.rut}')"

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "urlPDF": self.urlPDF,
            "rut": self.rut
            
        }

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
