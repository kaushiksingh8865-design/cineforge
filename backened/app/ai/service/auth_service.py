from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.models.user import User


class AuthService:

    @staticmethod
    async def get_user_by_username(
        db: AsyncSession,
        username: str,
    ) -> User | None:

        result = await db.execute(
            select(User).where(
                User.username == username
            )
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        username: str,
        password_hash: str,
    ) -> User:

        user = User(
            username=username,
            password=password_hash,
        )

        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user