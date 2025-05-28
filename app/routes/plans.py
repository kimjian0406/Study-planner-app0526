from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import StudyPlan
from datetime import datetime

plans_bp = Blueprint("plans", __name__)

# 📌 계획 등록
@plans_bp.route("/plans", methods=["POST"])
@jwt_required()
def create_plan():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_plan = StudyPlan(
        user_id=user_id,
        subject=data["subject"],
        plan=data["plan"],
        planned_date=datetime.strptime(data["planned_date"], "%Y-%m-%d").date(),
        is_completed=False
    )
    db.session.add(new_plan)
    db.session.commit()

    return jsonify({"msg": "Study plan created"}), 201

# 📌 나의 계획 전체 조회
@plans_bp.route("/plans", methods=["GET"])
@jwt_required()
def get_my_plans():
    user_id = get_jwt_identity()
    plans = StudyPlan.query.filter_by(user_id=user_id).all()
    result = []
    for p in plans:
        result.append({
            "id": p.id,
            "subject": p.subject,
            "plan": p.plan,
            "planned_date": p.planned_date.strftime("%Y-%m-%d"),
            "is_completed": p.is_completed
        })
    return jsonify(result), 200

# 📌 계획 완료 체크
@plans_bp.route("/plans/<int:plan_id>/complete", methods=["PATCH"])
@jwt_required()
def mark_complete(plan_id):
    user_id = get_jwt_identity()
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first()

    if not plan:
        return jsonify({"msg": "Plan not found"}), 404

    plan.is_completed = True
    db.session.commit()
    return jsonify({"msg": "Plan marked as completed"}), 200

