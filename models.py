from pydantic import BaseModel
from typing import Dict, Any

class Observation(BaseModel):
    input_text: str
    task_type: str
    step_number: int = 0
    context: Dict[str, Any] = {}

class Action(BaseModel):
    output: str

class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float] = {}
    feedback: str = ""