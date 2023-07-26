from fastapi import APIRouter, Depends, HTTPException, status

from app.lib.auth.prisma import JWTBearer, decodeJWT
from app.lib.prisma import prisma

import logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/users/me")
async def read_user_me(token=Depends(JWTBearer())):
    try:
        decoded = decodeJWT(token)
        if "userId" in decoded:
            userId = decoded["userId"]
            user = prisma.user.find_unique(where={"id": userId}, include={"profile": True})
            return {"success": True, "data": user}
        else:
            logger.error("userId not in JWT")
    except Exception as e:
        logger.error("Couldn't find user: {e}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {userId} not found",
    )


@router.get("/users/{userId}")
async def read_user(userId: str):
    try:
        user = prisma.user.find_unique(where={"id": userId}, include={"profile": True})
        if user:
            return {"success": True, "data": user}
        else:
            logger.error("Couldn't find user")
    except Exception as e:
        logger.error("Error finding user: {e}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with id {userId} not found",
    )
