from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.core.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    hash_password,
    verify_password,
)

from app.ai.database.database import get_db

from app.ai.models.user import User

from app.ai.schemas.auth import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)

from app.ai.service.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    existing_user = await AuthService.get_user_by_username(
        db,
        user.username,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered.",
        )

    hashed_password = hash_password(
        user.password,
    )

    created_user = await AuthService.create_user(
        db=db,
        username=user.username,
        password_hash=hashed_password,
    )

    return created_user


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):

    existing_user = await AuthService.get_user_by_username(
        db,
        user.username,
    )

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    if not verify_password(
        user.password,
        existing_user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        {
            "sub": str(existing_user.id),
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    current_user = result.scalar_one_or_none()

    if current_user is None:
        raise credentials_exception

    return current_user


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user