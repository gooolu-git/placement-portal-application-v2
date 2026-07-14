from flask import request,jsonify
from flask_restful import Resource
from auth import admin_required
from models import User, db,PlacementDrive , Application
from datetime import datetime
from sqlalchemy import func

class GetallUsers(Resource):
    @admin_required
    def get(self):
        try:
            users = User.query.filter_by(is_blacklisted=False, is_approved=True).all()
            serialized_user = []
            
            for user in users:
                u_dict = user.to_dict()
                # Attach profiles dynamically based on roles for the UI tables
                if user.role == 'student' and user.student_profile:
                    u_dict['student_profile'] = user.student_profile.to_dict()
                elif user.role == 'company' and user.company_profile:
                    u_dict['company_profile'] = user.company_profile.to_dict()
                serialized_user.append(u_dict)
                
            return {
                "status": "success",
                "count": len(users),
                "data": serialized_user
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"some error occurred {str(e)}"}, 500

class GetallUnactiveUSers(Resource):
    @admin_required
    def get(self):
        try:
            users = User.query.filter_by(is_approved=False).all()
            unactive_users = []
            
            for user in users:
                u_dict = user.to_dict()
                if user.role == 'student' and user.student_profile:
                    u_dict['student_profile'] = user.student_profile.to_dict()
                elif user.role == 'company' and user.company_profile:
                    u_dict['company_profile'] = user.company_profile.to_dict()
                unactive_users.append(u_dict)
                
            return {
                "status": "success",
                "count": len(unactive_users),
                "data": unactive_users
            }, 200
        except Exception as e:
            return {"status": "error", "message": f"some error occurred {str(e)}"}, 500 

class ApproveUnapproveUser(Resource):
    @admin_required
    def patch(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"status": "error", "message": "user not found "}, 404
            data = request.get_json() or {}
            new_status = data.get('is_approved')
            if new_status is None:
                return {"status": "error", "message": "the status is missing"}, 400
            if type(new_status) is not bool:
                return {"status": "typError", "message": "the provided status is not boolean"}, 400
            
            user.is_approved = new_status 
            db.session.commit()
            action_taken_text = 'approved' if new_status else "unapproved"
            return {
                "status": "success",
                "action": f"User '{user.username}' has been successfully {action_taken_text}.",
                "data": user.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": f"An error occurred while updating profile status: {str(e)}"
            }, 500

class BlockUnblockUser(Resource):
    @admin_required
    def patch(self, user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return {"status": "error", "message": "user not found "}, 404
            data = request.get_json() or {}
            new_status = data.get('is_blocked')
            if new_status is None:
                return {"status": "error", "message": "the status is missing"}, 400
            if type(new_status) is not bool:
                return {"status": "typError", "message": "the provided status is not boolean"}, 400
            
            user.is_blacklisted = new_status 
            db.session.commit()
            action_taken_text = 'blocked' if new_status else "unblocked"
            return {
                "status": "success",
                "action": f"User '{user.username}' has been successfully {action_taken_text}.",
                "data": user.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {
                "status": "error",
                "message": f"An error occurred while updating profile status: {str(e)}"
            }, 500

class GetUserDetails(Resource):
    @admin_required
    def get(self, user_id):
        try:
            user = db.session.get(User, user_id)
            if not user:
                return {"status": "error", "message": "user not found"}, 404
            
            u_dict = user.to_dict()
            if user.role == 'student' and user.student_profile:
                u_dict['student_profile'] = user.student_profile.to_dict()
            elif user.role == 'company' and user.company_profile:
                u_dict['company_profile'] = user.company_profile.to_dict()
                
            return {
                "status": "success",
                "data": u_dict
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error occurred : {str(e)}"
            }, 500

class GetCompanyFullDetails(Resource):
    @admin_required
    def get(self, user_id):
        try:
            user = db.session.get(User, user_id)
            if not user or user.role != 'company':
                return {"status": "error", "message": "Company not found"}, 404
            
            u_dict = user.to_dict()
            if user.company_profile:
                # Add profile details
                u_dict['company_profile'] = user.company_profile.to_dict()
                
                # Add drives with their applications
                drives_data = []
                for drive in user.company_profile.drives:
                    d_dict = drive.to_dict()
                    d_dict['applications'] = [app.to_dict() for app in drive.applications]
                    drives_data.append(d_dict)
                
                u_dict['drives'] = drives_data
                
            return {
                "status": "success",
                "data": u_dict
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500

class GetStudentFullDetails(Resource):
    @admin_required
    def get(self, user_id):
        try:
            user = db.session.get(User, user_id)
            if not user or user.role != 'student':
                return {"status": "error", "message": "Student not found"}, 404
            
            u_dict = user.to_dict()
            if user.student_profile:
                # Add basic student profile
                u_dict['student_profile'] = user.student_profile.to_dict()
                
                # Add applications with nested drive and company info
                apps_data = []
                for app in user.student_profile.applications:
                    a_dict = app.to_dict()
                    if app.target_drive:
                        d_dict = app.target_drive.to_dict()
                        # Include company name for the UI
                        if app.target_drive.company_owner:
                            d_dict['company_owner'] = {
                                'company_name': app.target_drive.company_owner.company_profile.company_name 
                                if app.target_drive.company_owner.company_profile else 'N/A'
                            }
                        a_dict['target_drive'] = d_dict
                    apps_data.append(a_dict)
                
                u_dict['student_profile']['applications'] = apps_data
                
            return {
                "status": "success",
                "data": u_dict
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 500


class AdminManageDrives(Resource):
    @admin_required
    def get(self):
        """Fetch all drives for the list view (DriveDirectory)"""
        search = request.args.get('search', '')
        query = PlacementDrive.query
        if search:
            query = query.filter(PlacementDrive.job_title.ilike(f'%{search}%'))
        drives = query.all()
        applications = Application.query.count()
        return {"status": "success", "data": [d.to_dict() for d in drives],"applicationcount":applications}, 200

class AdminDriveDetail(Resource):
    @admin_required
    def get(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive: return {"status": "error", "message": "Not found"}, 404
        company = drive.company_owner
        company_details = {}
        if company:
            company_details = {
                "id": company.id,
                "company_name": company.company_name,
                "website": company.website,
                "hr_contact": company.hr_contact,
                "hr_name": company.user.name if company.user else "Unknown",
                "is_approved": company.user.is_approved if company.user else False
            }
        applicants_list = []
        for app in drive.applications:
            student = app.student_applicant
            if student:
                applicants_list.append({
                    "application_id": app.id,
                    "applied_on": app.applied_on.strftime('%Y-%m-%d %H:%M'),
                    "status": app.status,
                    "student_details": {
                        "student_id": student.id,
                        "cgpa": student.cgpa,
                        "department": student.department,
                        "resume": student.resume,
                        "name": student.user.name if student.user else "Unknown",
                        "email": student.user.email if student.user else "Unknown",
                        "is_blacklisted": student.user.is_blacklisted if student.user else False
                    }
                })

        response_data = {
            "drive_details": {
                "id": drive.id,
                "job_title": drive.job_title,
                "job_description": drive.job_description,
                "eligiblity_criteria": drive.eligiblity_criteria,
                "deadline": drive.deadline.strftime('%Y-%m-%d %H:%M:%S'),
                "status": drive.status
            },
            "company_details": company_details,
            "applicants": applicants_list,
            "total_applicants": len(applicants_list)
        }
        return {"status":"success", "data": response_data}, 200

    @admin_required
    def patch(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if not drive: return {"status": "error", "message": "Not found"}, 404
        
        data = request.get_json()
        
        if 'status' in data: drive.status = data['status']
        if 'job_title' in data: drive.job_title = data['job_title']
        if 'job_description' in data: drive.job_description = data['job_description']
        if 'eligiblity_criteria' in data: drive.eligiblity_criteria = data['eligiblity_criteria']
        
        if 'deadline' in data:
            try:
                drive.deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    drive.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return {"status": "error", "message": "Invalid date format"}, 400
        
        db.session.commit()
        return {"status": "success", "message": "Drive updated", "data": drive.to_dict()}, 200
    
    
class ApproveDrive(Resource):
    @admin_required
    def patch(self, drive_id):
        try:
            drive = PlacementDrive.query.get(drive_id)
            if not drive:
                return {"status": "error", "message": "Placement drive not found"}, 404
            
            if drive.status == "pending":
                new_status = "Approved"
            elif drive.status == "Approved":
                new_status = "pending"
            else:
                return {
                    "status": "error", 
                    "message": f"Drive status is '{drive.status}'. Only 'pending' or 'Approved' drives can be toggled."
                }, 400

            drive.status = new_status
            db.session.commit()
            
            return {
                "status": "success",
                "message": f"Drive '{drive.job_title}' status updated to '{new_status}' successfully.",
                "data": drive.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 500