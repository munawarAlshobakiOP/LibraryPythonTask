from fastapi import HTTPException, Depends, APIRouter,Form
from sqlalchemy.orm import Session as DbSession
from typing import List
from uuid import UUID
from Database import  Session
from management.Schemas import Member, MemberCreate
import management.Models as Models
router = APIRouter()

@router.post("/members/", response_model=Member)
def create_member(member: MemberCreate=Form(...), db: DbSession = Depends(Session.get_db)):
    if db.query(Models.Member).filter(Models.Member.email == member.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_member = Models.Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

@router.get("/members/", response_model=List[Member])
def read_members(db: DbSession = Depends(Session.get_db)):
    members = db.query(Models.Member).all()
    if not members:
        raise HTTPException(status_code=404, detail="No members found")
    return members

@router.get("/members/{member_id}", response_model=Member)
def read_member(member_id: UUID, db: DbSession = Depends(Session.get_db)):
    member = db.query(Models.Member).filter(Models.Member.Id == member_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member
