import os
from werkzeug.utils import secure_filename
from flask_restful import Resource
from flask import request , current_app
from models import db , User , Student , Company
from auth import generate_token 
from flask_jwt_extended import jwt_required, get_jwt


class HandleRegister(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role')

        if not all([username, email, password, name, role]):
            return {"status": "error", "message": "All common fields are required"}, 400

        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"status": "error", "message": "Username or Email already registered"}, 400

        try:
            new_user = User(
                username=username,
                email=email,
                name=name,
                role=role
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()

            if role == 'student':
                new_student = Student(
                    user_id=new_user.id,
                    department=data.get('department'),
                    cgpa=float(data.get('cgpa', 0.0)),
                    resume=data.get('resume_link') 
                )
                db.session.add(new_student)

            elif role == 'company':
                company_name = data.get('company_name')
                if not company_name:
                    return {"status": "error", "message": "Company name is required"}, 400

                new_company = Company(
                    user_id=new_user.id,
                    company_name=company_name,
                    hr_contact=data.get('hr_contact'),
                    website=data.get('website')
                )
                db.session.add(new_company)

            db.session.commit()
            from tasks import send_registration_email
            send_registration_email.delay(new_user.email, new_user.name, user_id=new_user.username)
            
            return {
                "status": "success",
                "message": "User registered successfully!",
                "user": new_user.to_dict()
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"Server error: {str(e)}"}, 500    

class HandleLogin(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"status":"error","message":"Missing username or password"} , 400
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"status":"error", "message":"invalid Usernamer or Password"},400
        if not user.is_approved:
            return {"status":"error", "message":"Yet Not Verified by Admin"},400
        if user.is_blacklisted:
            return {"status":"error", "message":"You are Blocked by Admin"},400
        token = generate_token(user.id, user.username, user.role)
        return {
            "status": "success",
            "token": token,
            "user": user.to_dict()
        }, 200


class HandleUinqueEmail(Resource):
    def post(self):
        credential = request.get_json() or{}
        if not credential:
            return {
                "status":"error",
                "message":"data not received"
            },400
        
        email = credential.get('email',None)
        if not email:
            return {
                "status":"error",
                "message":"email not received"
            },400
        user = User.query.filter_by(email=email).first()
        if not user:
            return{
                "message":"available"
            },200
        return{
            "message":"unavailable"
        },200
class HandleUinqueUserName(Resource):
    def post(self):
        credential = request.get_json() or{}
        if not credential:
            return {
                "status":"error",
                "message":"data not received"
            },400
        
        username = credential.get('username',None)
        if not username:
            return {
                "status":"error",
                "message":"email not received"
            },400
        user = User.query.filter_by(username=username).first()
        if not user:
            return{
                "message":"available"
            },200
        return{
            "message":"unavailable"
        },200


class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt().get("sub")
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        response = user.to_dict()
        if user.role == 'student' and user.student_profile:
            response.update(user.student_profile.to_dict())
        elif user.role == 'company' and user.company_profile:
            response.update(user.company_profile.to_dict())
        return response, 200

    @jwt_required()
    def put(self):
        data = request.get_json()
        user_id = get_jwt().get("sub")
        user = User.query.get(user_id)
        
        if not user:
            return {"message": "User not found"}, 404
            
        current_password = data.get('cpassword')
        if not current_password or not user.check_password(current_password):
            return {"message": "Invalid current password. Authorization failed."}, 401
        
        user.name = data.get('name', user.name)
        
        if user.role == 'student' and user.student_profile:
            profile = user.student_profile
            profile.cgpa = data.get('cgpa', profile.cgpa)
            profile.department = data.get('department', profile.department)
            new_resume = data.get('resume_link')
            if new_resume is not None:
                profile.resume = new_resume            
        elif user.role == 'company' and user.company_profile:
            profile = user.company_profile
            profile.company_name = data.get('company_name', profile.company_name)
            profile.hr_contact = data.get('hr_contact', profile.hr_contact)
            profile.website = data.get('website', profile.website)
        
        new_password = data.get('npassword')
        if new_password:
            user.set_password(new_password)
            
        try:
            db.session.commit()
            return {"status": "success", "message": "Profile updated successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 500