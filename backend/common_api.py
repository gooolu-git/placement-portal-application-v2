from flask_restful import Resource
from flask import request 
from models import db , User
from auth import generate_token 

class HandleRegister(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        role = data.get('role') # 'student' or 'company'    
        if not all([username, email , password , name , role]):
            return {"status":"error","message":"all fields are required "}   , 400 
        if User.query.filter((User.username==username)|(User.email==email)).first():
            return {"status": "error", "message": "Username or Email already registered"}, 400
        try:
            new_user = User(
                username=username,
                email=email,
                name = name,
                role = role
            )
            new_user.set_password(password)
            db.session.add(new_user)
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
        if not user.is_blacklisted:
            return {"status":"error", "message":"You are Blocked by Admin"},400
        token = generate_token(user.id, user.username, user.role)
        return {
            "status": "success",
            "token": token,
            "user": user.to_dict()
        }, 200


