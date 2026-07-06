from flask import Flask
from flask_restful import Api, Resource
from models import db, User
from flask_jwt_extended import JWTManager
from config import Config
from common_api import HandleLogin , HandleRegister , HandleUinqueEmail,HandleUinqueUserName
from api.admin_api import GetallUsers
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

#===========admin_rotues_registration=============
api.add_resource(GetallUsers,'/admin/users')


@app.route('/')
def home():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)