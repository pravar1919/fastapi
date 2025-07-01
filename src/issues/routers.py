from fastapi import APIRouter, Depends, Response
from .schema import CreateIssue
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_sessions
from .service import IssueService

issues_router = APIRouter()
issue_service = IssueService()


@issues_router.post("/create_issue")
async def issues(data: CreateIssue, session: AsyncSession = Depends(get_sessions),):
    issue = await issue_service.create_issue(data, session)
    if issue:
        return Response("Issue Saved Successfully")
    return Response({"error": "Failed to save issue"}, status_code=400)

@issues_router.post("/get_all")
async def get_issues(session: AsyncSession = Depends(get_sessions),):
    issue = await issue_service.get_all_issues(session)
    return issue
