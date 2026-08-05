"""
Dependency injection – authentication removed.
All routes use a shared default guest user.
"""

import uuid

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User

# Fixed guest user ID – same UUID every time
GUEST_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


async def get_current_user(db: AsyncSession = Depends(get_db)) -> User:
    """
    Returns the default guest user.
    Creates it in the database if it doesn't exist yet.
    """
    result = await db.execute(select(User).where(User.id == GUEST_USER_ID))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            id=GUEST_USER_ID,
            email="guest@edupilot.ai",
            full_name="Guest User",
            hashed_password="no-auth",
            is_active=True,
            is_verified=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
