from flask import Flask
from flask_restful import Api, Resource
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Database initialization
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@institute.edu",  # Added missing required email field
            name="admin",
            role="admin",                 # Added role explicit definition
            is_admin=True,
            is_blacklisted=False,
            is_approved=True
        )
        admin.set_password('admin')
        
        # FIXED: Pass the variable object `admin`, NOT the string string `'admin'`
        db.session.add(admin)
        db.session.commit()
        print("Programmatic Admin successfully seeded!")

@app.route('/')
def home():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True)