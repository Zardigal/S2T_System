from fastapi import APIRouter

from fastapi_users import FastAPIUsers
from src.services.auth.auth import auth_backend
from src.services.auth.database import UserDb
from src.services.auth.manager import get_user_manager
from src.services.auth.schemas import UserCreate, UserRead


router = APIRouter(
    prefix='/auth',
)

fastapi_users = FastAPIUsers[UserDb, int](
    get_user_manager,
    [auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/jwt',
    tags=['Auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='',
    tags=['Auth'],
)
