import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models, schemas, dependencies

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/submissions/pending", response_model=List[schemas.SubmissionOut])
def get_pending_submissions(
    current_admin: models.User = Depends(dependencies.require_role("admin")),
    db: Session = Depends(get_db)
):
    submissions = db.query(models.Submission).filter(models.Submission.status == "pending").all()
    return submissions

@router.put("/submissions/{submission_id}/approve")
def approve_submission(
    submission_id: int,
    current_admin: models.User = Depends(dependencies.require_role("admin")),
    db: Session = Depends(get_db)
):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if submission.status != "pending":
        raise HTTPException(status_code=400, detail="Submission already processed")

    submission.status = "approved"
    submission.reviewed_at = datetime.utcnow()
    # Публикуем трек
    track = submission.track
    track.is_published = True
    db.commit()
    return {"message": "Submission approved"}

@router.put("/submissions/{submission_id}/reject")
def reject_submission(
    submission_id: int,
    current_admin: models.User = Depends(dependencies.require_role("admin")),
    db: Session = Depends(get_db)
):
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    if submission.status != "pending":
        raise HTTPException(status_code=400, detail="Submission already processed")

    submission.status = "rejected"
    submission.reviewed_at = datetime.utcnow()
    db.commit()
    return {"message": "Submission rejected"}