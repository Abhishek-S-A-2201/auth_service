from sqlalchemy.orm import Session
from . import models, auth_utils
from datetime import datetime


def create_user(db: Session, email: str, password: str):
    hashed_password = auth_utils.get_password_hash(password)
    user = models.User(email=email, password=hashed_password,
                       created_at=int(datetime.now().timestamp()))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_organization(db: Session, name: str, personal: bool, settings: dict):
    org = models.Organization(name=name, personal=personal,
                              settings=settings, created_at=int(datetime.now().timestamp()))
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def add_role(db: Session, name: str, description: str, org_id: int):
    role = models.Role(name=name, description=description, org_id=org_id)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def add_member(db: Session, org_id: int, user_id: int, role_id: int):
    member = models.Member(org_id=org_id, user_id=user_id,
                           role_id=role_id, created_at=int(datetime.now().timestamp()))
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def get_member_by_org_and_user(db: Session, org_id: int, user_id: int):
    return db.query(models.Member).filter(models.Member.org_id == org_id, models.Member.user_id == user_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_member_by_org_and_user(db: Session, org_id: int, user_id: int):
    return db.query(models.Member).filter(models.Member.org_id == org_id, models.Member.user_id == user_id).first()


def get_org_by_name(db: Session, name: str):
    return db.query(models.Organization).filter(models.Organization.name == name).first()


def update_password(db: Session, user: models.User, new_password: str):
    hashed_password = auth_utils.get_password_hash(new_password)
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    return user


def delete_member(db: Session, org_id: int, user_id: int):
    member = get_member_by_org_and_user(db, org_id, user_id)
    if member:
        db.delete(member)
        db.commit()
    return member


def update_member_role(db: Session, org_id: int, user_id: int, new_role_id: int):
    member = get_member_by_org_and_user(db, org_id, user_id)
    if member:
        member.role_id = new_role_id
        db.commit()
        db.refresh(member)
    return member
