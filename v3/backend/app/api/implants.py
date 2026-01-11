from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

router = APIRouter(prefix="/api/implants", tags=["implants"])

# Data Models
class ImplantStatus(str, Enum):
    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    CALIBRATION = "calibration"
    ACTIVE = "active"
    DEGRADED = "degraded"

class NeuralImplant(BaseModel):
    id: str
    name: str
    category: str
    description: str
    status: ImplantStatus
    progress: int  # 0-100%
    skill_points: int
    prerequisites: List[str]
    estimated_time: str
    icon_type: str
    difficulty: str  # "Beginner", "Intermediate", "Advanced"

class ImplantListResponse(BaseModel):
    implants: List[NeuralImplant]
    categories: List[str]

class ImplantDetailResponse(BaseModel):
    implant: NeuralImplant
    learning_objectives: List[str]
    next_steps: str
    recommended_practice: str

# Mock Data
MOCK_IMPLANTS = [
    NeuralImplant(
        id="impl_001",
        name="Blue Ocean Strategy",
        category="Strategy",
        description="Master untapped market opportunities through value innovation",
        status=ImplantStatus.CALIBRATION,
        progress=65,
        skill_points=250,
        prerequisites=[],
        estimated_time="4 hours",
        icon_type="compass",
        difficulty="Intermediate"
    ),
    NeuralImplant(
        id="impl_002",
        name="Negotiation Mastery",
        category="Sales",
        description="Advanced techniques for high-stakes business negotiations",
        status=ImplantStatus.ACTIVE,
        progress=100,
        skill_points=180,
        prerequisites=[],
        estimated_time="3 hours",
        icon_type="handshake",
        difficulty="Advanced"
    ),
    NeuralImplant(
        id="impl_003",
        name="Emotional Intelligence 2.0",
        category="HR",
        description="Decode and influence team dynamics with precision",
        status=ImplantStatus.AVAILABLE,
        progress=0,
        skill_points=200,
        prerequisites=["impl_002"],
        estimated_time="5 hours",
        icon_type="brain",
        difficulty="Intermediate"
    ),
    NeuralImplant(
        id="impl_004",
        name="Data-Driven Decision Making",
        category="Tech",
        description="Transform raw data into strategic advantages",
        status=ImplantStatus.DOWNLOADING,
        progress=35,
        skill_points=220,
        prerequisites=[],
        estimated_time="6 hours",
        icon_type="chart",
        difficulty="Advanced"
    ),
    NeuralImplant(
        id="impl_005",
        name="Agile Leadership",
        category="Strategy",
        description="Lead high-performance teams in dynamic environments",
        status=ImplantStatus.AVAILABLE,
        progress=0,
        skill_points=190,
        prerequisites=["impl_003"],
        estimated_time="4 hours",
        icon_type="users",
        difficulty="Advanced"
    ),
    NeuralImplant(
        id="impl_006",
        name="Financial Modeling",
        category="Tech",
        description="Build and analyze complex financial projections",
        status=ImplantStatus.AVAILABLE,
        progress=0,
        skill_points=240,
        prerequisites=["impl_004"],
        estimated_time="7 hours",
        icon_type="calculator",
        difficulty="Advanced"
    )
]

@router.get("", response_model=ImplantListResponse)
async def get_implants(category: Optional[str] = None, status: Optional[str] = None):
    """
    Get all available neural implants.
    Can filter by category and status.
    """
    implants = MOCK_IMPLANTS
    
    if category:
        implants = [i for i in implants if i.category.lower() == category.lower()]
    
    if status:
        implants = [i for i in implants if i.status == status]
    
    categories = list(set(i.category for i in MOCK_IMPLANTS))
    
    return ImplantListResponse(
        implants=implants,
        categories=categories
    )

@router.get("/active")
async def get_active_implants():
    """Get currently active implants."""
    active = [i for i in MOCK_IMPLANTS if i.status == ImplantStatus.ACTIVE]
    return {"active_implants": active}

@router.get("/{implant_id}", response_model=ImplantDetailResponse)
async def get_implant_detail(implant_id: str):
    """Get detailed information about a specific implant."""
    implant = next((i for i in MOCK_IMPLANTS if i.id == implant_id), None)
    
    if not implant:
        return {"error": "Implant not found"}, 404
    
    # Mock learning objectives
    objectives_map = {
        "impl_001": [
            "Identify untapped market spaces",
            "Create value innovation frameworks",
            "Execute blue ocean moves"
        ],
        "impl_002": [
            "Master BATNA analysis",
            "Deploy advanced persuasion tactics",
            "Handle difficult counterparties"
        ],
        "impl_003": [
            "Recognize emotional patterns",
            "Build authentic team connections",
            "Navigate workplace conflicts"
        ]
    }
    
    return ImplantDetailResponse(
        implant=implant,
        learning_objectives=objectives_map.get(implant_id, ["Complete module", "Pass assessment", "Apply knowledge"]),
        next_steps="Begin calibration session to activate this implant",
        recommended_practice="Daily 15-minute sessions for optimal retention"
    )

@router.post("/{implant_id}/download")
async def download_implant(implant_id: str):
    """Initiate implant download process."""
    implant = next((i for i in MOCK_IMPLANTS if i.id == implant_id), None)
    
    if not implant:
        return {"error": "Implant not found"}, 404
    
    return {
        "status": "success",
        "message": f"Download initiated for {implant.name}",
        "estimated_completion": "2 minutes"
    }

@router.post("/{implant_id}/calibrate")
async def calibrate_implant(implant_id: str):
    """Start calibration session for an implant."""
    implant = next((i for i in MOCK_IMPLANTS if i.id == implant_id), None)
    
    if not implant:
        return {"error": "Implant not found"}, 404
    
    return {
        "status": "success",
        "message": "Calibration session initiated",
        "session_id": f"cal_{implant_id}_{hash(implant_id) % 10000}",
        "exercises": 5
    }
