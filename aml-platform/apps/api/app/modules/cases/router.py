import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.entities import Case, CaseAlert, CaseNote, Alert
from app.schemas.contracts import CaseCreate, CaseNoteIn, DispositionIn
from app.services.audit_service import record
router=APIRouter(prefix="/api/v1/cases",tags=["cases"])
@router.post("")
def create_case(body:CaseCreate,db:Session=Depends(get_db)):
    alerts=[db.get(Alert,x) for x in body.alert_ids]
    if any(x is None for x in alerts): raise HTTPException(404,"Alert not found")
    cid=str(uuid.uuid4()); obj=Case(id=cid,case_ref="CASE-"+cid[:8].upper(),priority=body.priority,owner_id=body.owner_id)
    db.add(obj)
    for a in alerts:
        db.add(CaseAlert(id=str(uuid.uuid4()),case_id=cid,alert_id=a.id)); a.status="in_review"
    record(db,body.owner_id,"case_created","case",cid,after={"alert_ids":body.alert_ids})
    db.commit(); return obj
@router.get("")
def list_cases(db:Session=Depends(get_db)): return list(db.scalars(select(Case).order_by(Case.opened_at.desc())))
@router.get("/{case_id}")
def get_case(case_id:str,db:Session=Depends(get_db)):
    obj=db.scalar(select(Case).where((Case.id==case_id)|(Case.case_ref==case_id)))
    if not obj: raise HTTPException(404,"Case not found")
    return {"case":obj,"notes":list(db.scalars(select(CaseNote).where(CaseNote.case_id==obj.id))),
      "alerts":list(db.scalars(select(Alert).join(CaseAlert,CaseAlert.alert_id==Alert.id).where(CaseAlert.case_id==obj.id)))}
@router.post("/{case_id}/notes")
def add_note(case_id:str,body:CaseNoteIn,db:Session=Depends(get_db)):
    obj=db.scalar(select(Case).where((Case.id==case_id)|(Case.case_ref==case_id)))
    if not obj: raise HTTPException(404,"Case not found")
    note=CaseNote(id=str(uuid.uuid4()),case_id=obj.id,author_id=body.author_id,note=body.note)
    db.add(note); record(db,body.author_id,"case_note_added","case",obj.id,after={"note_id":note.id})
    db.commit(); return {"status":"saved","note_id":note.id}
@router.post("/{case_id}/disposition")
def set_disposition(case_id:str,body:DispositionIn,db:Session=Depends(get_db)):
    allowed={"false_positive","explainable_activity","escalate","further_information_required"}
    if body.disposition not in allowed: raise HTTPException(422,{"allowed":sorted(allowed)})
    obj=db.scalar(select(Case).where((Case.id==case_id)|(Case.case_ref==case_id)))
    if not obj: raise HTTPException(404,"Case not found")
    before={"status":obj.status,"disposition":obj.disposition}
    obj.status="closed" if body.disposition!="further_information_required" else "pending_information"
    obj.disposition=body.disposition
    if obj.status=="closed": obj.closed_at=datetime.now(timezone.utc)
    record(db,body.actor_id,"disposition_recorded","case",obj.id,before=before,after={"status":obj.status,"disposition":body.disposition,"note":body.note})
    db.commit(); return {"status":obj.status,"disposition":obj.disposition}
