from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, auth_utils, dependencies
from app.models import User, Organization, Member, Role
import time
from ..auth_utils import get_password_hash


router = APIRouter()


@router.post("/auth/signup")
def sign_up(user: schemas.UserCreate, org_details: schemas.OrganizationCreate, db: Session = Depends(dependencies.get_db)):

    # Check if the email already exists
    existing_user = db.query(User).filter(
        User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create the new user
    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        profile={},
        status=0,
        settings={},
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    db.add(new_user)
    db.commit()

    # Create the new organization
    new_organization = Organization(
        name=org_details.name,
        status=0,
        personal=False,
        settings={},
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    db.add(new_organization)
    db.commit()

    new_role = Role(
        name="Owner",
        description="Owner of the organization",
        org_id=new_organization.id,
    )
    db.add(new_role)
    db.commit()

    # Add the member entry
    new_member = Member(
        org_id=new_organization.id,
        user_id=new_user.id,
        role_id=new_role.id,
        status=0,
        settings={},
        created_at=int(time.time()),
        updated_at=int(time.time())
    )
    db.add(new_member)
    db.commit()

    return {"message": "User and organization created successfully"}


@router.post("/auth/signin", response_model=schemas.Token)
def sign_in(user: schemas.UserLogin, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not auth_utils.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = auth_utils.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/reset_password")
def reset_password(user: schemas.UserResetPassword, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = auth_utils.get_password_hash(user.new_password)
    db_user.password = hashed_password
    db.commit()
    db.refresh(db_user)

    return {"message": "Password has been updated successfully"}
