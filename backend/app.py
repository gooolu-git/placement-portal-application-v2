from flask import Flask
from flask_restful import Api, Resource
from models import db, User
from flask_jwt_extended import JWTManager
from config import Config
from common_api import HandleLogin , HandleRegister , HandleUinqueEmail,HandleUinqueUserName ,Profile
from api.admin_api import GetallUsers,GetallUnactiveUSers,ApproveUnapproveUser,BlockUnblockUser,GetUserDetails,GetCompanyFullDetails,GetStudentFullDetails,AdminDriveDetail,AdminManageDrives,ApproveDrive
from api.company_api import CreateDrive,GetApplicantList,GetUserApplications,UpdateApplicationStatus,CompanyDashboard,GetSelectedCandidates
from api.student_api import StudentDashboard, ApplyToDrive, ApplicationHistory, ApplicationTracking,ExportApplications

from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db.init_app(app)
jwt = JWTManager(app)
CORS(app,origins=['http://localhost:5173','http://localhost:5000'])

# Database initialization
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@institute.edu",
            name="admin",
            role="admin",                 
            is_admin=True,
            is_blacklisted=False,
            is_approved=True
        )
        admin.set_password('adminn')
        db.session.add(admin)
        db.session.commit()




api.add_resource(HandleLogin,"/login")
api.add_resource(HandleRegister,"/register")
api.add_resource(HandleUinqueEmail,'/uniquemail')
api.add_resource(HandleUinqueUserName,'/uniqueusername')
api.add_resource(Profile,'/profile')

#===========admin_api=============
api.add_resource(GetallUsers, '/admin/users')
api.add_resource(GetallUnactiveUSers, '/admin/unactive-users')
api.add_resource(ApproveUnapproveUser, '/admin/approve/<int:user_id>')
api.add_resource(BlockUnblockUser, '/admin/block/<int:user_id>')
api.add_resource(GetUserDetails, '/admin/user/<int:user_id>')
api.add_resource(GetCompanyFullDetails, '/admin/company/<int:user_id>')
api.add_resource(GetStudentFullDetails, '/admin/student/<int:user_id>')
api.add_resource(AdminManageDrives, '/admin/drives')
api.add_resource(AdminDriveDetail, '/admin/drive/<int:drive_id>')
api.add_resource(ApproveDrive, '/admin/drive/approve/<int:drive_id>')

#===========company_related_api's ================
api.add_resource(CompanyDashboard, '/company/dashboard')
api.add_resource(CreateDrive, '/company/drive/create')
api.add_resource(GetApplicantList, '/company/drive/<int:drive_id>/applicants')
api.add_resource(GetUserApplications, '/company/student/<int:applicant_id>/applications')
api.add_resource(UpdateApplicationStatus, '/company/application/<int:application_id>/status')
api.add_resource(GetSelectedCandidates, '/company/selected-candidates')

#====================stdents_api's=============================
api.add_resource(StudentDashboard, '/student/dashboard')
api.add_resource(ApplyToDrive, '/student/apply/<int:drive_id>')
api.add_resource(ApplicationHistory, '/student/history')
api.add_resource(ApplicationTracking, '/student/tracking')
api.add_resource(ExportApplications, '/student/export-applications')


@app.route('/')
def home():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)