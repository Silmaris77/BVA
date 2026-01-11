from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from v2.backend.database import get_db
from v2.backend import models, schemas, auth

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("", response_model=List[schemas.LessonResponse])
def get_lessons(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Get all lessons with completion status for current user"""
    lessons = db.query(models.Lesson).order_by(models.Lesson.order).all()
    
    # Get user progress
    progress_map = {
        p.lesson_id: p.completed 
        for p in db.query(models.LessonProgress).filter(models.LessonProgress.user_id == current_user.id).all()
    }
    
    result = []
    for lesson in lessons:
        # Convert SQLAlchemy model to Pydantic schema manually to inject 'completed'
        # or use from_orm if schema allows, but we need to set the extra field
        lesson_data = schemas.LessonResponse.from_orm(lesson)
        lesson_data.completed = progress_map.get(lesson.id, False)
        result.append(lesson_data)
        
    return result

@router.get("/{lesson_id}", response_model=schemas.LessonResponse)
def get_lesson(lesson_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    progress = db.query(models.LessonProgress).filter(
        models.LessonProgress.user_id == current_user.id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()
    
    lesson_resp = schemas.LessonResponse.from_orm(lesson)
    if progress:
        lesson_resp.completed = progress.completed
        
    return lesson_resp

@router.post("/{lesson_id}/complete")
def complete_lesson(lesson_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    lesson = db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    progress = db.query(models.LessonProgress).filter(
        models.LessonProgress.user_id == current_user.id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()
    
    xp_gained = 0
    
    if not progress:
        # First time completion
        progress = models.LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=True,
            watched_duration=lesson.duration
        )
        db.add(progress)
        
        # Award XP
        current_user.xp += lesson.xp_reward
        current_user.degencoins += int(lesson.xp_reward / 10)
        xp_gained = lesson.xp_reward
        
        # Log activity
        log = models.ActivityLog(
            user_id=current_user.id, # Using ID integer
            activity_type="completed_lesson", # Matches schema
            description=f"Ukończono lekcję: {lesson.title}",
            xp_awarded=lesson.xp_reward
        )
        db.add(log)
    else:
        # Already exists, ensure marked as completed
        if not progress.completed:
             progress.completed = True
             current_user.xp += lesson.xp_reward
             xp_gained = lesson.xp_reward
             # Log activity
             log = models.ActivityLog(
                user_id=current_user.id,
                activity_type="completed_lesson",
                description=f"Ukończono lekcję: {lesson.title}",
                xp_awarded=lesson.xp_reward
             )
             db.add(log)

    db.commit()
    return {"status": "completed", "xp_gained": xp_gained, "total_xp": current_user.xp}
