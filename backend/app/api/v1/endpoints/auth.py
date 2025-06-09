from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services.email import send_welcome_email

router = APIRouter()


@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserRegister,
) -> any:
    """Register new user."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user_create = schemas.UserCreate(
        email=user_in.email, password=user_in.password, full_name=user_in.full_name
    )
    user = crud.user.create(db, obj_in=user_create)

    # Send welcome email asynchronously
    try:
        send_welcome_email(user.email, user.full_name or "User")
    except Exception as e:
        print(f"Failed to send welcome email: {e}")

    return user


@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> any:
    """OAuth2 compatible token login."""
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> any:
    """Get current user."""
    return current_user
