from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Niche


class NicheService:

    @staticmethod
    def create_niche(
        name: str,
        description: str = "",
    ) -> Niche:

        with SessionLocal() as session:
            niche = Niche(
                name=name,
                description=description,
            )

            session.add(niche)
            session.commit()
            session.refresh(niche)

            return niche

    @staticmethod
    def get_niches() -> list[Niche]:

        with SessionLocal() as session:
            statement = select(Niche).order_by(
                Niche.name
            )

            return list(
                session.scalars(statement).all()
            )

    @staticmethod
    def search_niches(
        search_term: str,
    ) -> list[Niche]:

        with SessionLocal() as session:
            statement = (
                select(Niche)
                .where(
                    Niche.name.ilike(
                        f"%{search_term}%"
                    )
                )
                .order_by(Niche.name)
            )

            return list(
                session.scalars(statement).all()
            )
