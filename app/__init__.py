from flask import Flask
from flask_login import LoginManager
from .models import db, User
from .routes import home, auth  # 🔥 auth 라우터 추가

def create_app():
    app = Flask(__name__)

 # 세션용 시크릿키
    app.config['SECRET_KEY'] = 'dev-key'

    # DB 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planner.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # DB 초기화
    db.init_app(app)

    # 로그인 매니저 설정
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 블루프린트 등록
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.auth)

    # 테이블 생성
    with app.app_context():
        db.create_all()

    return app
