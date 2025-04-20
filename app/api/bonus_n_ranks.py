from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from app.api_clients.auth import AuthApiClient
from app.api_clients.mlm import MLMApiClient
from app.api_clients.mlm import MLMApiClient
from app.schemas.bonus import BonusCreate
from app.schemas.token import Token
from app.schemas.user import UserOut
from app.utils.logs import get_logger

logger = get_logger(__name__)

router = APIRouter()
mlm_client = MLMApiClient.prepare()
auth_client = AuthApiClient.prepare()

@router.post("/distribute")
async def distribute_bonus(payload: BonusCreate):
    return await mlm_client.trigger_bonus({
        "source_user_id": str(payload.source_user_id),
        "trigger_type": payload.trigger_type
    })

@router.get("/history")
async def get_bonus_history(token: str = Header("Authorization")):
    """
    Get bonus history for the mlmenticated user.
    """
    user = await auth_client.get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Assuming the MLM API has an endpoint to get downline users
    mlm_client = MLMApiClient.prepare()
    response = await mlm_client.get_user_bonus_history(str(user.get('id')))
    
    return response

@router.post("/")
async def list_bonuses():
    """
    list all the bonuses
    """
    # Assuming the MLM API has an endpoint to get downline users
    response = await mlm_client.get_all_bonus()
    
    if not response:
        raise HTTPException(status_code=404, detail="Bonus not found")
    
    return response

@router.post("/mark-paid/{bonus_id}")
async def mark_bonus_paid(bonus_id: UUID):
    """
    Mark a bonus as paid
    """
    # Assuming the MLM API has an endpoint to get downline users
    response = await mlm_client.mark_bonus_paid(str(bonus_id))
    
    if not response:
        raise HTTPException(status_code=404, detail="Downline not found")
    
    return response

@router.post("/pay-all")
async def pay_all_bonuses():
    """
    Pay all bonuses
    """
    # Assuming the MLM API has an endpoint to get downline users
    response = await mlm_client.pay_all_bonuses()
    
    if not response:
        raise HTTPException(status_code=404, detail="Downline not found")
    
    return response

@router.get("/weekly-report")
async def get_weekly_bonus_report(token: str = Header("Authorization")):
    """
    Get weekly bonus report for the authenticated user.
    """
    user = await auth_client.get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Assuming the MLM API has an endpoint to get downline users
    response = await mlm_client.get_user_weekly_bonus_report(str(user.get('id')))
    
    if not response:
        raise HTTPException(status_code=404, detail="Downline not found")
    
    return response

@router.get("/user-rank")
async def get_user_rank(token: str = Header("Authorization")):
    """
    Get user rank for the authenticated user.
    """
    user = await auth_client.get_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Assuming the MLM API has an endpoint to get downline users
    response = await mlm_client.get_user_rank(str(user.get('id')))
    
    if not response:
        raise HTTPException(status_code=404, detail="Downline not found")
    
    return response