from flask_restful import Resource
from auth import admin_required
from models import User
from flask import request


class GetallUsers(Resource):
    @admin_required
    def get(self):
        try:
            users = User.query.filter_by(is_blacklisted=False , is_approved = True).all()
            serialized_uesr = [user.to_dict() for user in users]
            return {
                "status":"success",
                "count":len(users),
                "data":serialized_uesr
            },200
        except Exception as e:
            return {"status":"error","message":f"some error occured {str(e)}"},500
class GetallUnactiveUSers(Resource):
    @admin_required
    def get(self):
        try:
            users = User.query.filter_by(is_approved=False).all()
            unactive_users = [users.to_dict() for user in users]
            return {
                "status":"success",
                "count":len(unactive_users),
                "data":unactive_users
            },200
        except Exception as e:
            return {"status":"error","message":f"some error occured{str(e)}"} , 500 
class ApproveUnapproveUser(Resource):
    @admin_required
    def patch(self,user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"status":"error","message":"user not found "},404
            data = request.get_json() or {}
            new_status = data.get('is_approved')
            if new_status is None:
                return {"status":"error","message":"the status is missing"}
            if(type(new_status) is not bool):
                return {"status":"typError","message":"the provided status is not boolean"},400
            user.is_approved= new_status 
            db.session.commit()
            action_taken_text = 'approved' if new_status else "unapproved"
            return {
                "status":"success",
                "action":f"User '{user.username}' has been successfully {action_taken_text}.",
                "data":user.to_dict()
            },200
        except Exception as e:
            db.session.rollback()
            return {
                "status":"error",
                "message":f"An error occurred while updating profile status: {str(e)}"
            },500
class BlockUnblockUser(Resource):
    @admin_required
    def patch(self,user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"status":"error","message":"user not found "},404
            data = request.get_json() or {}
            new_status = data.get('is_blocked')
            if new_status is None:
                return {"status":"error","message":"the status is missing"}
            if(type(new_status) is not bool):
                return {"status":"typError","message":"the provided status is not boolean"}
            user.is_approved= new_status 
            db.session.commit()
            action_taken_text = 'blocked' if new_status else "unblocked"
            return {
                "status":"success",
                "action":f"User '{user.username}' has been successfully {action_taken_text}.",
                "data":user.to_dict()
            },200
        except Exception as e:
            db.session.rollback()
            return {
                "status":"error",
                "message":f"An error occurred while updating profile status: {str(e)}"
            },500

def GetUserDetails(Resource):
    @admin_required
    def get(self,user_id):
        try:
            user = db.session.get(User,user_id)
            if not user:
                return {"status":"error","message":"user not found"},404
            return{
                "status":"success",
                "data":user
            },200

        except Exception as e:
            return{
                "status":"error",
                "message":f"Error occured : {str(e)}"
            },500
