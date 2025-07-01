from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import CreateIssue
from src.db.models import Issue
from sqlmodel import select, desc


class IssueService:
    async def create_issue(self, data: CreateIssue, session: AsyncSession):
        issue_dict = data.model_dump()

        issue_obj = Issue(**issue_dict)
        session.add(issue_obj)
        await session.commit()
        return issue_obj
    
    async def get_all_issues(self, session: AsyncSession):
        statement = select(Issue).order_by(desc(Issue.created_at))

        result = await session.exec(statement)
        if not result:
            return None
        return result.all()
