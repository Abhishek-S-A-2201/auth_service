from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, dependencies

router = APIRouter()


@router.post("/member/invite")
def invite_member(invite: schemas.InviteMember, db: Session = Depends(dependencies.get_db)):

    user = crud.get_user_by_email(db, invite.email)
    org = crud.get_org_by_name(db, invite.org_name)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    role = crud.add_role(
        db, name="Member", description="Member of the organization", org_id=org.id)

    crud.add_member(db, org_id=org.id,
                    user_id=user.id, role_id=role.id)

    return {"message": f"User invited to organization {org.name}"}


@router.delete("/member/delete")
def delete_member(delete_member: schemas.DeleteMember, db: Session = Depends(dependencies.get_db)):

    user = crud.get_user_by_email(db, delete_member.user_email)
    org = crud.get_org_by_name(db, delete_member.org_name)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    member = crud.get_member_by_org_and_user(
        db, org_id=org.id, user_id=user.id)

    if not member:
        raise HTTPException(
            status_code=404, detail="Member not found in this organization")

    db.delete(member)
    db.commit()

    return {"message": "Member deleted successfully"}


@router.put("/member/update_role")
def update_member_role(update_member_role: schemas.UpdateMemberRole, db: Session = Depends(dependencies.get_db)):

    user = crud.get_user_by_email(db, update_member_role.user_email)
    org = crud.get_org_by_name(db, update_member_role.org_name)
    role = crud.get_role_by_name(db, update_member_role.new_role)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    if not role:
        role = crud.add_role(
            db, name=update_member_role.new_role, description="Member", org_id=org.id)

    member = crud.get_member_by_org_and_user(
        db, org_id=org.id, user_id=user.id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.role_id = role.id
    db.commit()
    db.refresh(member)

    return {"message": "Member role updated successfully"}
