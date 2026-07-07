from flask import request
from flask_restful import Resource
from auth import admin_required
from models import User, db,PlacementDrive

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
        return {"status": "success", "data": [d.to_dict() for d in drives]}, 200

class AdminDriveDetail(Resource):
    @admin_required
    def get(self, drive_id):
        """Fetch full details + applicants for the DriveProfile page"""
        drive = PlacementDrive.query.get(drive_id)
        if not drive: return {"status": "error", "message": "Not found"}, 404
        
        d_dict = drive.to_dict()
        # Include list of applications with applicant details
        d_dict['applications'] = [app.to_dict() for app in drive.applications]
        return {"status": "success", "data": d_dict}, 200

    @admin_required
    def patch(self, drive_id):
        """Update drive status, title, or description"""
        drive = PlacementDrive.query.get(drive_id)
        if not drive: return {"status": "error", "message": "Not found"}, 404
        
        data = request.get_json()
        if 'status' in data: drive.status = data['status']
        if 'job_title' in data: drive.job_title = data['job_title']
        if 'deadline' in data: drive.deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M')
        
        db.session.commit()
        return {"status": "success", "message": "Drive updated"}, 200

class ApproveDrive(Resource):
    @admin_required
    def patch(self, drive_id):
        """
        Approves a pending placement drive.
        """
        try:
            drive = PlacementDrive.query.get(drive_id)
            if not drive:
                return {"status": "error", "message": "Placement drive not found"}, 404
            
            # Ensure we are only approving drives that are currently pending
            if drive.status != "pending":
                return {
                    "status": "error", 
                    "message": f"Drive is currently '{drive.status}', cannot approve."
                }, 400

            drive.status = "Approved"
            db.session.commit()
            
            return {
                "status": "success",
                "message": f"Drive '{drive.job_title}' has been approved successfully.",
                "data": drive.to_dict()
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 500