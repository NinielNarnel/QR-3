from app import app, db, login_manager
from flask_login import LoginManager
from app.models import User
from flask_login import LoginManager

login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    