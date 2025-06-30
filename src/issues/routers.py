from fastapi import APIRouter, Depends
from .schema import CreateIssue
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_sessions

issues_router = APIRouter()


@issues_router.post("/create_issue")
def issues(data: CreateIssue, session: AsyncSession = Depends(get_sessions),):
    print(data)
