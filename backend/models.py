from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'admin', 'company', 'student'
    name = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    
    # Relationships
    student_profile = db.relationship('Student', backref='user', uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship('Company', backref='user', uselist=False, cascade="all, delete-orphan")
    
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
        
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_admin": self.is_admin,
            "is_blacklisted": self.is_blacklisted,
            "is_approved": self.is_approved
        }


class Company(db.Model):
    __tablename__ = 'company'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    hr_contact = db.Column(db.String(50), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    
    drives = db.relationship('PlacementDrive', backref="company_owner", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "hr_contact": self.hr_contact,
            "website": self.website,
            "is_approved": self.user.is_approved if self.user else False,
            "is_blacklisted": self.user.is_blacklisted if self.user else False
        }


class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cgpa = db.Column(db.Float, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    resume = db.Column(db.String(255), nullable=True)
    
    # Changed backref from 'student_application' to 'student_applicant' to match Application model dictionary helper
    applications = db.relationship('Application', backref='student_applicant', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else "Unknown",
            "username": self.user.username if self.user else "Unknown",
            "cgpa": self.cgpa,
            "department": self.department,
            "resume": self.resume,
            "is_blacklisted": self.user.is_blacklisted if self.user else False
        }


class PlacementDrive(db.Model):
    __tablename__ = 'placement_drive'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False) # Changed from String to Integer
    job_title = db.Column(db.String(250), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligiblity_criteria = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default="pending")
    
    applications = db.relationship('Application', backref='target_drive', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company_owner.company_name if self.company_owner else "Unknown",
            "job_title": self.job_title,
            "job_description": self.job_description,
            "eligiblity_criteria": self.eligiblity_criteria,
            "deadline": self.deadline.strftime('%Y-%m-%d %H:%M:%S'),
            "status": self.status
        }


class Application(db.Model):
    __tablename__ = 'application'
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_student_drive_application'),
    ) 
    
    id = db.Column(db.Integer, primary_key=True) # Fixed primary_key syntax
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False) # Fixed ForeignKey syntax
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Applied') # Fixed syntax and quotes

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student_applicant.user.name if self.student_applicant and self.student_applicant.user else "Unknown",
            "drive_id": self.drive_id,
            "job_title": self.target_drive.job_title if self.target_drive else "Unknown",
            "company_name": self.target_drive.company_owner.company_name if self.target_drive and self.target_drive.company_owner else "Unknown",
            "applied_on": self.applied_on.strftime('%Y-%m-%d %H:%M'),
            "status": self.status
        }



