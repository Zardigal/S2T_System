from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin
from src.services.auth.config import JWT_SECRET
from src.services.auth.database import UserDb, get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[UserDb, int]):
    reset_password_token_secret = JWT_SECRET
    verification_token_secret = JWT_SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
