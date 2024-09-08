from fastapi import APIRouter, Depends, Query
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.master_proposals.services import MasterProposalCrud
from src.master_proposals.schemas import CreateMasterProposal, GetMasterProposal


router = APIRouter(
    prefix="/master",
    tags=["Master"]
)


current_active_user = fastapi_users.current_user(active=True)


@router.post("/proposal", status_code=201)
async def create_proposal(proposal: CreateMasterProposal, session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_active_user)):
    return await MasterProposalCrud.create_proposal(proposal, session, user)


@router.get("/proposal/{id}", status_code=200)
async def get_single_proposal(proposal_id: int, session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_active_user)):
    return await MasterProposalCrud.get_proposal_by_id(proposal_id, session, user)
