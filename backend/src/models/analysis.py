from pydantic import BaseModel
from typing import List


# A single output models
class ReadingAnalysis(BaseModel):
    RoomChoice: str
    Readings: str
    RuleCategory: str
    Rule: str
    Status: str
    Explanation: str


# Multiple outputs
class Analysis(BaseModel):
    results: List[ReadingAnalysis]
