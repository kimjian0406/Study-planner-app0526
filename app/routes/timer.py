from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import TimerLog
from datetime import datetime

timer_bp = Blueprint("timer", __name__)

# 타이머 시작
@timer_bp.route("/timer/start", methods=["POST"])
@jwt_required()
def start_timer():
    user_id = get_jwt_identity()
    data = request.get_json()
    subject = data.get("subject")

    timer = TimerLog(user_id=user_id, subject=subject)
    db.session.add(timer)
    db.session.commit()

    return jsonify({
        "msg": "Timer started",
        "timer_id": timer.id,
        "start_time": timer.start_time.strftime("%Y-%m-%d %H:%M:%S")
    }), 201

# 타이머 종료
@timer_bp.route("/timer/<int:timer_id>/stop", methods=["PATCH"])
@jwt_required()
def stop_timer(timer_id):
    user_id = get_jwt_identity()
    timer = TimerLog.query.filter_by(id=timer_id, user_id=user_id).first()

    if not timer:
        return jsonify({"msg": "Timer not found"}), 404

    if timer.end_time:
        return jsonify({"msg": "Timer already stopped"}), 400

    timer.end_time = datetime.utcnow()
    delta = timer.end_time - timer.start_time
    timer.duration_minutes = int(delta.total_seconds() // 60)
    db.session.commit()

    return jsonify({
        "msg": "Timer stopped",
        "duration_minutes": timer.duration_minutes,
        "start_time": timer.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": timer.end_time.strftime("%Y-%m-%d %H:%M:%S")
    }), 200

# 타이머 기록 전체 조회
@timer_bp.route("/timer/logs", methods=["GET"])
@jwt_required()
def get_logs():
    user_id = get_jwt_identity()
    timers = TimerLog.query.filter_by(user_id=user_id).order_by(TimerLog.start_time.desc()).all()

    results = []
    for t in timers:
        results.append({
            "id": t.id,
            "subject": t.subject,
            "start_time": t.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": t.end_time.strftime("%Y-%m-%d %H:%M:%S") if t.end_time else None,
            "duration_minutes": t.duration_minutes
        })

    return jsonify(results), 200

