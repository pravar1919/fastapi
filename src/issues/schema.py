from pydantic import BaseModel
import uuid
from datetime import datetime, date
from enum import Enum


class IssueStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    HOLD = "HOLD"

class CreateIssue(BaseModel):
    title: str
    description: str
