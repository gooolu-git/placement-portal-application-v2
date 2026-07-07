from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt
from datetime import datetime
from auth import company_required
from models import db, User, PlacementDrive, Application, Student

# --- NEW: Company Dashboard API ---
class CompanyDashboard(Resource):
    @company_required
    def get(self):
        try:
            claims = get_jwt()
            user_id = claims.get("sub")
            user = db.session.get(User, user_id)
            
            if not user or not user.company_profile:
                return {"status": "error", "message": "Company profile not found"}, 404
            
            # Get all drives for this company
            drives = PlacementDrive.query.filter_by(company_id=user.company_profile.id).all()
            
            return {
                "status": "success",
                "company": user.company_profile.to_dict(),
                "drives": [d.to_dict() for d in drives]
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"Error loading dashboard: {str(e)}"}, 500

# --- EXISTING RESOURCES ---

class CreateDrive(Resource):
    @company_required
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"status": "error", "message": "Payload is missing"}, 400
            
            claims = get_jwt()
            user_id = claims.get("sub")
            user = db.session.get(User, user_id)
            
            if not user.company_profile:
                return {"status": "error", "message": "Company profile not found"}, 404
                
            deadline_str = data.get('deadline')
            deadline_obj = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

            new_drive = PlacementDrive(
                company_id=user.company_profile.id,
                job_title=data.get('job_title'),
                job_description=data.get('job_description'),
                eligiblity_criteria=data.get('eligiblity_criteria'),
                deadline=deadline_obj
            )
            db.session.add(new_drive)
            db.session.commit()
            
            return {
                "status": "success",
                "message": f"Drive {new_drive.job_title} created successfully",
                "data": new_drive.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"Error occurred: {str(e)}"}, 500

class GetApplicantList(Resource):
    @company_required
    def get(self, drive_id):
        try:
            drive = db.session.get(PlacementDrive, drive_id)
            if not drive:
                return {"status": "error", "message": "Invalid Drive id"}, 404
            
            serialized_apps = [app.to_dict() for app in drive.applications]
            return {
                "status": "success",
                "count": len(serialized_apps),
                "data": serialized_apps
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"An Error Occurred: {str(e)}"}, 500

class GetUserApplications(Resource):
    @company_required
    def get(self, applicant_id):
        try:
            applicant = db.session.get(Student, applicant_id)
            if not applicant:
                return {"status": "error", "message": "Student not found"}, 404
            
            serialized_apps = [app.to_dict() for app in applicant.applications]
            return {
                "status": "success",
                "data": serialized_apps
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"An Error occurred: {str(e)}"}, 500

class UpdateApplicationStatus(Resource):
    @company_required
    def patch(self, application_id):
        try:
            application = db.session.get(Application, application_id)
            if not application:
                return {"status": "error", "message": "Application record not found"}, 404
                
            data = request.get_json() or {}
            new_status = data.get('status') 
            
            allowed_statuses = ['Pending', 'Shortlisted', 'Selected', 'Rejected']
            if new_status not in allowed_statuses:
                return {"status": "error", "message": f"Invalid status. Choose from {allowed_statuses}"}, 400
                
            application.status = new_status
            db.session.commit()
            
            return {
                "status": "success",
                "message": f"Status updated to {new_status}",
                "data": application.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"An Error occurred: {str(e)}"}, 500


class GetSelectedCandidates(Resource):
    @company_required
    def get(self):
        try:
            claims = get_jwt()
            user_id = claims.get("sub")
            user = db.session.get(User, user_id)
            
            if not user or not user.company_profile:
                return {"status": "error", "message": "Company profile not found"}, 404
            
            # Query applications where status is 'Selected' AND the drive belongs to this company
            selected_apps = Application.query.join(PlacementDrive).filter(
                Application.status == 'Selected',
                PlacementDrive.company_id == user.company_profile.id
            ).all()
            
            return {
                "status": "success",
                "count": len(selected_apps),
                "data": [app.to_dict() for app in selected_apps]
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"An Error occurred: {str(e)}"}, 500