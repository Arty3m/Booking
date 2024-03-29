from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.schemas import SchemeUserAuth
from app.users.service import UserService
from app.users.model import Users

router = APIRouter(prefix='/auth',
                   tags=['Auth & Пользователи'])


@router.post('/register')
async def register_user(user_data: SchemeUserAuth):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(password=user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SchemeUserAuth):
    user: Users = await authenticate_user(user_data.email, user_data.password)
    if not user:
        return IncorrectEmailOrPasswordException
    access_token: str = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
