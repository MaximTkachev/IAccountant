from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import (
    UserCreate,
    Token
)
from ..services.auth import AuthService
from ..models.auth import User
from ..services.auth import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.post('/register', response_model=Token)
def create_a_new_user(user_data: UserCreate, service: AuthService = Depends()):
    return service.register_new_user(user_data)


@router.post('/login', response_model=Token)
def login_a_user_into_system(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(
        form_data.username,
        form_data.password
    )

