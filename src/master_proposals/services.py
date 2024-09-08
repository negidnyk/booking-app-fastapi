from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from src.master_proposals.models import MasterProposal
from src.master_proposals.schemas import CreateMasterProposal, GetMasterProposal
from src.users.user.validations import is_user, is_master


class MasterProposalCrud:
    @staticmethod
    async def create_proposal(proposal_details, session, user):

        try:
            stmt = insert(MasterProposal).values(service_id=proposal_details.service_id,
                                                 price=proposal_details.price,
                                                 description=proposal_details.description)
            await session.execute(stmt)
            await session.commit()

            query = select(MasterProposal).limit(1).order_by(MasterProposal.created_at.desc())
            created_proposal = await session.execute(query)
            result = created_proposal.scalar_one_or_none()

            return GetMasterProposal(id=result.id,
                                     service_id=result.service_id,
                                     price=result.price,
                                     description=result.description,
                                     created_at=result.created_at)
        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in create master proposal api service. Details:\n{e}")

    @staticmethod
    async def get_proposal_by_id(proposal_id, session, user):

        try:
            query = select(MasterProposal).where(MasterProposal.id == proposal_id)
            proposal = await session.execute(query)
            result = proposal.scalar_one_or_none()

            return GetMasterProposal(id=result.id,
                                     service_id=result.service_id,
                                     price=result.price,
                                     description=result.description,
                                     created_at=result.created_at)

        except Exception as e:
            raise HTTPException(status_code=500,
                                detail=f"Something went wrong in get master proposal api service. Details:\n{e}")