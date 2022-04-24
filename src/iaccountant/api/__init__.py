from fastapi import APIRouter

from .auth import router as auth_router
from .operations import router as operation_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(operation_router)