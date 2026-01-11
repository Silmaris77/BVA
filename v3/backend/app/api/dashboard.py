from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["dashboard"])

# Response Models
class OperatorStats(BaseModel):
    xp: int
    xp_change: str
    vc: int
    vc_level: int
    neural_link_status: str
    neural_link_latency: str

class Mission(BaseModel):
    id: str
    icon_type: str
    title: str
    subtitle: str
    reward_xp: str
    reward_vc: Optional[str] = None
    action: str
    is_crisis: bool = False

class TopOperator(BaseModel):
    rank: int
    name: str
    score: int
    is_current_user: bool = False

class CompetenceData(BaseModel):
    labels: List[str]
    values: List[int]

class DashboardResponse(BaseModel):
    operator_name: str
    stats: OperatorStats
    missions: List[Mission]
    top_operators: List[TopOperator]
    competence: CompetenceData
    system_status: str
    calendar_sync: str

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard():
    """
    Get complete dashboard data for the War Room.
    Returns operator stats, active missions, leaderboard, and competence radar.
    """
    return DashboardResponse(
        operator_name="Admin Unit",
        stats=OperatorStats(
            xp=2450,
            xp_change="+12% vs last week",
            vc=340,
            vc_level=3,
            neural_link_status="Stable",
            neural_link_latency="12ms"
        ),
        missions=[
            Mission(
                id="mission_001",
                icon_type="book",
                title="Protocol: Blue Ocean Strategy",
                subtitle="Implant Calibration Required",
                reward_xp="+50 XP",
                reward_vc="10 VC",
                action="Initialize",
                is_crisis=False
            ),
            Mission(
                id="mission_002",
                icon_type="alert",
                title="CRISIS: Client Churn Risk",
                subtitle="Execute retention protocol immediately",
                reward_xp="+200 XP",
                action="Engage",
                is_crisis=True
            )
        ],
        top_operators=[
            TopOperator(rank=1, name="Anna.K", score=4500, is_current_user=False),
            TopOperator(rank=2, name="Marek.Z", score=4120, is_current_user=False),
            TopOperator(rank=15, name="YOU", score=2450, is_current_user=True)
        ],
        competence=CompetenceData(
            labels=['Strategy', 'Verbal', 'Non-Verbal', 'Relations', 'Tech'],
            values=[85, 65, 90, 75, 60]
        ),
        system_status="ONLINE",
        calendar_sync="ACTIVE"
    )
