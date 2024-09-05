from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Role, Member, Organization
from typing import Optional

router = APIRouter()


@router.get("/stats/role-wise-users")
def get_role_wise_users(db: Session = Depends(get_db)):
    result = db.query(
        Role.name,
        func.count(User.id).label("user_count")
    ).join(Member, Role.id == Member.role_id).join(User, User.id == Member.user_id).group_by(Role.id).all()

    return {"role_wise_users": [{"name": r.name, "user_count": r.user_count} for r in result]}


@router.get("/stats/org-wise-members")
def get_org_wise_members(db: Session = Depends(get_db)):
    result = db.query(
        Organization.name,
        func.count(Member.id).label("member_count")
    ).join(Member, Organization.id == Member.org_id).group_by(Organization.id).all()

    return {"org_wise_members": [{"name": r.name, "member_count": r.member_count} for r in result]}


@router.get("/stats/org-role-wise-users")
def get_org_role_wise_users(from_date: Optional[int] = None, to_date: Optional[int] = None, status: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(
        Organization.name.label("organization"),
        Role.name.label("role"),
        func.count(User.id).label("user_count")
    ).join(Member, Organization.id == Member.org_id).join(Role, Member.role_id == Role.id).join(User, User.id == Member.user_id)

    if from_date:
        query = query.filter(User.created_at >= from_date)
    if to_date:
        query = query.filter(User.created_at <= to_date)
    if status is not None:
        query = query.filter(User.status == status)

    result = query.group_by(Organization.id, Role.id).all()

    return {"org_role_wise_users": [{"organization": r.organization, "role": r.role, "user_count": r.user_count} for r in result]}
