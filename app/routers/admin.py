
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.user import User
from app.models.enums import UserRole
from app.auth import require_role
from app.services import auth as auth_service
from app.services import users as user_service


router = APIRouter(prefix="/admin", tags=["Admin"])


# POST /admin/users
@router.post("/users", status_code=status.HTTP_201_CREATED)
def admin_create_user(
    data: dict = Body(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(require_role([UserRole.ADMIN])),
):
    
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", UserRole.USER.value)

    if not email:
        raise HTTPException(status_code=400, detail="email is required")
   
    if not password:
        raise HTTPException(status_code=400, detail="password is required")
   
   
    if user_service.get_user_by_email(session, email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
   
    password_hash = auth_service.hash_password(password)
   
    user = user_service.create_user(
        session=session,
        email=email,
        password_hash=password_hash,
        role=role
    )
   
    return user.to_dict()

