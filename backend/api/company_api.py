from flask_restful import Resource 
from flask import request
from models import PlacementDrive ,Application,Student
from flask_jwt_extended import get_jwt
from auth import company_required

class CreateDrive(Resource):
    @company_required
    def post(self):
        try:
            data = request.get_json()
            if data is None:
                return {
                    "status":"error",
                    "message":"Please fill all the fields"
                },404
            claims = get_jwt()
            user_id  = claims.get("sub")
            user = db.session.get(User,user_id)
            company_id=user.id
            new_drive = PlacementDrive(
                company_id=company_id,
                job_title=data.get('job_title'),
                job_description=data.get('job_description'),
                eligiblity_criteria=data.get('eligiblity_criteria'),
                deadline=data.get('deadline')
            )
            db.session.add(new_drive)
            db.session.commit()
            return {
                "staus":"success",
                "message":f"Drive {job_title} created successfully",
                data:new_drive
            }
        except Exception as e:
            return {
                "status":"error",
                "message":f"Error occured : {str(e)}"
            }


class GetApplicantList(Resource):
    @company_required
    def get(self,drive_id):
        try:
            drive = db.session.get(PlacementDrive,drive_id)
            if not drive:
                return {
                    "status":"Error",
                    "message":f"Invalid Drive id"
                },404
            applications = drive.applications
            serialized_apps = [app.to_dict() for app in applications]
            return{
                "status":"success",
                "message":"Applications are there",
                "data":serialized_apps
            },200
        except Exception as e:
            return {
                "staus":"error",
                "message":f"An Error Occured {str(e)}"
            },500

class GetUserApplications(Resource):
    @company_required
    def get(self,applicant_id):
        try:
            applicant = db.session.get(Student,applicant_id)
            data = applicant.applications
            if not data:
                return{
                    "status":"success",
                    "message":"No application found for this user",
                    "data":None
                }
            return{
                "status":"success",
                "message":f"Application list found for {applicant_id}",
                "data":data
            }
        except Exception as e:
            return{
                "status":"error",
                "message":f"An Error occured: {str(e)}"
            }
class UpdateApplicationStatus(Resource):
    @company_required
    def patch(self,application_id):
        try:
            application = db.session.get(Application, application_id)
            if not application:
                return {"status": "error", "message": "Application record not found"},404
                
            data = request.get_json() or {}
            new_status = data.get('status') 
            
            if not new_status:
                return {"status": "error", "message": "Status field is missing from payload data"}, 400
                
            application.status = new_status
            db.session.commit()
            
            return {
                "status": "success",
                "message": f"Application status updated to {new_status} successfully",
                "data": application.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"An Error occurred: {str(e)}"}, 500