from datetime import datetime

import pytz
from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)

user = Table(
    'user',
    metadata,

    # Default
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False, unique=True),
    Column('hashed_password', String, nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),

    # App specific
    Column('username', String, nullable=False, unique=True),
    Column('registered_at', TIMESTAMP(timezone=True), default=datetime.now(pytz.UTC)),
    Column('role_id', Integer, ForeignKey(role.c.id)),

    UniqueConstraint('email', 'username', name='uq_user_email_username')
)
