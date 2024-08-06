from datetime import datetime

import pytz
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.services.auth.models import role

class Base(DeclarativeBase):
    pass


class UserDb(SQLAlchemyBaseUserTable[int], Base):
    # Default
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # App specific
    username: Mapped[int] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(pytz.UTC)
    )
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey(role.c.id))


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserDb)
