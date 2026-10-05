from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Subniche


class SubnicheService:

    @staticmethod
    def create_subniche(
        niche_id: int,
        name: str,
        description: str = "",
    ) -> Subniche:

        with SessionLocal() as session:
            subniche = Subniche(
                niche_id=niche_id,
                name=name,
                description=description,
            )

            session.add(subniche)
            session.commit()
            session.refresh(subniche)

            return subniche

    @staticmethod
    def get_subniches(
        niche_id: int,
    ) -> list[Subniche]:

        with SessionLocal() as session:
            statement = (
                select(Subniche)
                .where(
                    Subniche.niche_id == niche_id
                )
                .order_by(Subniche.name)
            )

            return list(
                session.scalars(statement).all()
            )
