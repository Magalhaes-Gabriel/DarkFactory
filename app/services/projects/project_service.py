from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Project


class ProjectService:

    @staticmethod
    def create_project(
        name: str,
        topic: str,
        category: str,
    ) -> Project:

        with SessionLocal() as session:
            project = Project(
                name=name,
                topic=topic,
                category=category,
            )

            session.add(project)
            session.commit()
            session.refresh(project)

            return project

    @staticmethod
    def get_projects() -> list[Project]:

        with SessionLocal() as session:
            statement = select(Project).order_by(
                Project.created_at.desc()
            )

            return list(session.scalars(statement).all())

    @staticmethod
    def get_project(project_id: int) -> Project | None:

        with SessionLocal() as session:
            return session.get(Project, project_id)
