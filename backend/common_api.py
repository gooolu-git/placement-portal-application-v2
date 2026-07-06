import os
import base64
from werkzeug.utils import secure_filename
from flask_restful import Resource
from flask import request , current_app
from models import db , User , Student
from auth import generate_token 


class HandleRegister(Resource):
    def post(self):
        # 1. Parse JSON data
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role')  # 'student' or 'company' or 'admin'

        # 2. Check for required common fields
        if not all([username, email, password, name, role]):
            return {"status": "error", "message": "All common fields are required"}, 400

        # 3. Check if username or email already exists
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return {"status": "error", "message": "Username or Email already registered"}, 400

        try:
            # 4. Create the base User
            new_user = User(
                username=username,
                email=email,
                name=name,
                role=role
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()  # Flushes to get the new_user.id without committing yet

            # 5. Handle Student-specific fields
            if role == 'student':
                department = data.get('department')
                cgpa = data.get('cgpa')
                
                # Handling file upload via JSON (Base64 string format)
                resume_filename = None
                resume_b64 = data.get('resume_b64')  # Expecting base64 string
                orig_filename = data.get('resume_name', 'resume.pdf') # Expecting original file name

                if resume_b64:
                    filename = secure_filename(f"{username}_resume_{orig_filename}")
                    upload_path = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
                    if not os.path.exists(upload_path):
                        os.makedirs(upload_path)
                    
                    # Decode and save the file
                    with open(os.path.join(upload_path, filename), "wb") as fh:
                        fh.write(base64.b64decode(resume_b64))
                    resume_filename = filename

                new_student = Student(
                    user_id=new_user.id,
                    department=department,
                    cgpa=float(cgpa) if cgpa else 0.0,
                    resume=resume_filename
                )
                db.session.add(new_student)

            # 6. Handle Company-specific fields
            elif role == 'company':
                company_name = data.get('company_name')
                hr_contact = data.get('hr_contact')
                website = data.get('website')

                if not company_name:
                    return {"status": "error", "message": "Company name is required for company role"}, 400

                new_company = Company(
                    user_id=new_user.id,
                    company_name=company_name,
                    hr_contact=hr_contact,
                    website=website
                )
                db.session.add(new_company)

            # 7. Commit everything together safely
            db.session.commit()

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
