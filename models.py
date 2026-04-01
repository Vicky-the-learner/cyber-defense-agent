from pydantic import BaseModel, Field
from typing import List, Optional


class CyberAction(BaseModel):
    action: str  # BLOCK_IP / SANITIZE_INPUT / ALLOW


class CyberObservation(BaseModel):
    input: str
    attack: str
    confidence: float
    message: str


class CyberState(BaseModel):
    episode_id: Optional[str] = None
    step_count: int = 0
    history: List[dict] = Field(default_factory=list)