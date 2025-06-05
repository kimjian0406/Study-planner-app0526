from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Task

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, pw):
            login_user(user)
            return redirect(url_for('home.index'))
        else:
            flash('❌ 로그인 정보가 올바르지 않습니다.')
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자입니다.')
        else:
            user = User(username=username, password=generate_password_hash(pw))
            db.session.add(user)
            db.session.commit()
            flash('✅ 가입이 완료되었습니다. 로그인 해주세요!')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/mypage')
@login_required
def mypage():
    return render_template('mypage.html', theme=session.get('theme', 'light'))

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # 사용자 계정 삭제 시 연결된 할 일도 함께 삭제
    Task.query.filter_by(user_id=current_user.id).delete()
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash('계정이 삭제되었습니다.')
    return redirect(url_for('auth.login'))

