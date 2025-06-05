from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user, login_required
from app.models import Task, db
from datetime import datetime, date

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    selected_category = request.args.get('category')
    show_today = request.args.get('today') == '1'
    sort_priority = request.args.get('priority') == '1'
    search_keyword = request.args.get('search', '').strip()

    query = Task.query.filter_by(user_id=current_user.id)

    if selected_category:
        query = query.filter(Task.category == selected_category)
    if show_today:
        query = query.filter(Task.date == date.today())
    if search_keyword:
        query = query.filter(Task.content.ilike(f"%{search_keyword}%"))

    tasks = query.all()

    if sort_priority:
        def priority_value(t):
            return {'상': 0, '중': 1, '하': 2}.get(t.priority, 3)
        tasks.sort(key=priority_value)

    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    remaining = total - done
    today_tasks = [t for t in tasks if t.date == date.today()]
    categories = sorted(set(t.category for t in Task.query.filter_by(user_id=current_user.id) if t.category))

    return render_template(
        'index.html',
        tasks=tasks,
        total=total,
        done=done,
        remaining=remaining,
        today_count=len(today_tasks),
        selected_category=selected_category,
        categories=categories,
        show_today=show_today,
        sort_priority=sort_priority,
        theme=session.get('theme', 'light')  # ✅ 다크모드 연동
    )

@bp.route('/add', methods=['POST'])
@login_required
def add():
    content = request.form.get('task')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    category = request.form.get('category')
    notes = request.form.get('notes')
    priority = request.form.get('priority')

    if content and date_str:
        task_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        task = Task(
            content=content,
            date=task_date,
            time=time_str,
            category=category,
            notes=notes,
            priority=priority,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('home.index'))

@bp.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('home.index'))

@bp.route('/toggle/<int:task_id>')
@login_required
def toggle(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:
        task.done = not task.done
        db.session.commit()
    return redirect(url_for('home.index'))

@bp.route('/calendar')
@login_required
def calendar():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    events = []
    for t in tasks:
        events.append({
            "title": f"{t.content} ({t.category})" if t.category else t.content,
            "start": t.date.strftime('%Y-%m-%d'),
        })
    return render_template('calendar.html', events=events, theme=session.get('theme', 'light'))

@bp.route('/stats')
@login_required
def stats():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    categories = {}
    for t in tasks:
        if t.category:
            categories[t.category] = categories.get(t.category, 0) + 1
    return render_template('stats.html', total=total, done=done, categories=categories, theme=session.get('theme', 'light'))

@bp.route('/toggle-theme')
@login_required
def toggle_theme():
    current = session.get('theme', 'light')
    session['theme'] = 'dark' if current == 'light' else 'light'
    return redirect(request.referrer or url_for('home.index'))

