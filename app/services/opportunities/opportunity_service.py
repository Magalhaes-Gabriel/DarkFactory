from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import Opportunity


class OpportunityService:

    @staticmethod
    def create_opportunity(
        niche_id: int,
        title: str,
        subniche_id: int | None = None,
        description: str = "",
        potential: str = "medium",
        source: str = "",
    ) -> Opportunity:

        with SessionLocal() as session:
            opportunity = Opportunity(
                niche_id=niche_id,
                subniche_id=subniche_id,
                title=title,
                description=description,
                potential=potential,
                source=source,
            )

            session.add(opportunity)
            session.commit()
            session.refresh(opportunity)

            return opportunity

    @staticmethod
    def get_opportunities(
        niche_id: int | None = None,
        subniche_id: int | None = None,
    ) -> list[Opportunity]:

        with SessionLocal() as session:

            statement = select(
                Opportunity
            ).order_by(
                Opportunity.created_at.desc()
            )

            if niche_id is not None:
                statement = statement.where(
                    Opportunity.niche_id == niche_id
                )

            if subniche_id is not None:
                statement = statement.where(
                    Opportunity.subniche_id
                    == subniche_id
                )

            return list(
                session.scalars(statement).all()
            )

    @staticmethod
    def update_status(
        opportunity_id: int,
        status: str,
    ) -> None:

        with SessionLocal() as session:

            opportunity = session.get(
                Opportunity,
                opportunity_id,
            )

            if opportunity is None:
                return

            opportunity.status = status

            session.commit()

