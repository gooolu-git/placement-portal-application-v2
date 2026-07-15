from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt
from datetime import datetime
from auth import student_required
from models import db, PlacementDrive, Application, Student




def get_student_id_from_user():
    claims = get_jwt()
    user_id = claims.get("sub")
    student = Student.query.filter_by(user_id=user_id).first()
    return student.id if student else None

class StudentDashboard(Resource):
    @student_required
    def get(self):
        student_id = get_student_id_from_user()
        if not student_id: return {"status": "error", "message": "Profile not found"}, 404
        
        search_query = request.args.get('search', '').strip()
        query = PlacementDrive.query.filter(
            PlacementDrive.status == "Approved",
            PlacementDrive.deadline > datetime.now()
        )

        if search_query:
            query = query.filter(PlacementDrive.job_title.ilike(f'%{search_query}%'))
        
        drives = query.all()
        user_apps = Application.query.filter_by(student_id=student_id).all()
        
        return {
            "drives": [d.to_dict() for d in drives],
            "applied_drive_ids": [app.drive_id for app in user_apps]
        }, 200

class ApplyToDrive(Resource):
    @student_required
    def post(self, drive_id):
        student_id = get_student_id_from_user()
        if not student_id: return {"status": "error", "message": "Profile not found"}, 404
        
        drive = PlacementDrive.query.get_or_404(drive_id)
        
        if drive.deadline < datetime.now():
            return {"status": "error", "message": "Registration closed"}, 400

        existing = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
        if existing:
            return {"status": "error", "message": "Already applied"}, 400

        try:
            new_app = Application(
                student_id=student_id,
                drive_id=drive_id,
                status='Applied',
                applied_on=datetime.now()
            )
            db.session.add(new_app)
            db.session.commit()
            return {"status": "success", "message": f"Applied for {drive.job_title}"}, 201
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 500

class ApplicationHistory(Resource):
    @student_required
    def get(self):
        student_id = get_student_id_from_user()
        if not student_id: 
            return {"status": "error", "message": "Profile not found"}, 404
        
        history = Application.query.join(PlacementDrive).filter(
            Application.student_id == student_id,
            PlacementDrive.status == 'Approved' 
        ).all()
        
        return {"data": [app.to_dict() for app in history]}, 200

class ApplicationTracking(Resource):
    @student_required
    def get(self):
        student_id = get_student_id_from_user()
        if not student_id: return {"status": "error", "message": "Profile not found"}, 404
        
        applications = Application.query.filter_by(student_id=student_id).all()
        
        return {"data": [app.to_dict() for app in applications]}, 200



class ExportApplications(Resource):

    @student_required 
    def post(self):
        student_id = get_student_id_from_user() 
        if not student_id:
            return {"status": "error", "message": "Student profile not found"}, 404
        student_record = Student.query.get(student_id)
        from tasks import ExportApplications
        ExportApplications.delay(
                    student_id=student_id,
                    student_email=student_record.user.email,
                    student_name=student_record.user.name
                )
        
        return {"status": "success", "message": "Your report is being generated and will be emailed to you shortly."}, 202



