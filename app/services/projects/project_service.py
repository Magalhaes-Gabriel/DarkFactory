from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Project


class ProjectService:
    @staticmethod
    def create_project(
        name: str,
        topic: str,
        category: str,
        niche_id: int | None = None,
        subniche_id: int | None = None,
        opportunity_id: int | None = None,
        script: str | None = None,
    ) -> Project:
        with SessionLocal() as session:
            project = Project(
                name=name,
                topic=topic,
                category=category,
                niche_id=niche_id,
                subniche_id=subniche_id,
                opportunity_id=opportunity_id,
                script=script,
            )

            session.add(project)
            session.commit()
            session.refresh(project)

            return project

    @staticmethod
    def get_projects() -> list[Project]:
        with SessionLocal() as session:
            statement = (
                select(Project)
                .order_by(Project.created_at.desc())
            )

            return list(
                session.scalars(statement).all()
            )

    @staticmethod
    def get_project(
        project_id: int,
    ) -> Project | None:
        with SessionLocal() as session:
            return session.get(Project, project_id)

    @staticmethod
    def update_script(
        project_id: int,
        script: str,
    ) -> Project | None:
        with SessionLocal() as session:
            project = session.get(
                Project,
                project_id,
            )

            if project is None:
                return None

            project.script = script

            session.commit()
            session.refresh(project)

            return project

    @staticmethod
    def update_status(project_id: int, status: str,) -> Project | None:
        with SessionLocal() as session:
            project = session.get(
                Project,
                project_id,
            )

            if project is None:
                return None

            project.status = status

            session.commit()
            session.refresh(project)

            return project