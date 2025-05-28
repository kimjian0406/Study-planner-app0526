from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import TimerLog
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

# 오늘 공부 요약
@dashboard_bp.route("/dashboard/today", methods=["GET"])
@jwt_required()
def get_today_summary():
    user_id = get_jwt_identity()
    now = datetime.utcnow()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1)

    timers = TimerLog.query.filter(
        TimerLog.user_id == user_id,
        TimerLog.end_time >= start_of_day,
        TimerLog.end_time < end_of_day
    ).all()

    total_minutes = sum(t.duration_minutes or 0 for t in timers)

    return jsonify({
        "date": now.strftime("%Y-%m-%d"),
        "total_minutes": total_minutes,
        "hours": total_minutes // 60,
        "minutes": total_minutes % 60
    })

# 최근 7일 공부 요약
@dashboard_bp.route("/dashboard/week", methods=["GET"])
@jwt_required()
def get_week_summary():
    user_id = get_jwt_identity()
    today = datetime.utcnow().date()
    start_day = today - timedelta(days=6)

    timers = TimerLog.query.filter(
        TimerLog.user_id == user_id,
        TimerLog.end_time != None,
        TimerLog.start_time >= datetime.combine(start_day, datetime.min.time())
    ).all()

    total_minutes = sum(t.duration_minutes or 0 for t in timers)

    return jsonify({
        "from": start_day.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d"),
        "total_minutes": total_minutes,
        "hours": total_minutes // 60,
        "minutes": total_minutes % 60
    })

