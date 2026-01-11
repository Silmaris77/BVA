from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class UserBase(BaseModel):
    username: str

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    avatar_url: Optional[str] = None
    degen_type: Optional[str] = None
    preferences: Optional[dict] = None


class UserStats(BaseModel):
    username: str
    xp: int
    level: int
    degencoins: int
    degen_type: Optional[str] = None
    company: Optional[str] = None
    joined_date: Optional[date] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserPublic(BaseModel):
    username: str
    xp: int
    level: int
    degencoins: int
    degen_type: Optional[str] = None
    company: Optional[str] = None
    
    class Config:
        from_attributes = True

class ActivityLogBase(BaseModel):
    activity_type: str
    description: Optional[str] = None
    xp_awarded: int = 0
    timestamp: datetime

class ActivityLog(ActivityLogBase):
    id: int
    
    class Config:
        from_attributes = True

# --- Milwaukee Tools Schemas ---

class MilwaukeeContext(BaseModel):
    typ_klienta: str
    typ_pracy: str
    materialy_srodowisko: List[str]
    skala: str

class MilwaukeeAppMatch(BaseModel):
    app_id: str
    score: float
    reason: str
    details: Dict[str, Any]

class DiscoveryQuestion(BaseModel):
    id: str
    question: str
    type: str # choice, multi_choice, scale, yes_no, number
    options: Optional[List[str]] = None
    scale: Optional[List[str]] = None
    purpose: Optional[str] = None

class RecommendationRequest(BaseModel):
    app_id: str
    answers: Dict[str, Any] # q_id -> answer

class RecommendationPackage(BaseModel):
    package: Dict[str, Any] # narzedzia, baterie, etc.
    persuasion_script: Optional[Dict[str, Any]] = None
    roi_calculator: Optional[Dict[str, Any]] = None
    case_studies: Optional[List[Dict[str, Any]]] = None

# --- LESSONS SCHEMAS ---

class LessonBase(BaseModel):
    id: str
    title: str
    description: str
    category: str
    video_url: str
    thumbnail_url: Optional[str] = None
    duration: int
    xp_reward: int
    difficulty: str

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    completed: bool = False
    
    class Config:
        from_attributes = True

class LessonProgressUpdate(BaseModel):
    completed: bool
    watched_duration: int

