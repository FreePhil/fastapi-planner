from fastapi import HTTPException, status, APIRouter

from models.users import UserSignIn

user_router = APIRouter(
    tags=['User']
)

users = {}


@user_router.post('/signup')
async def sign_new_user(data: UserSignIn) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with supplied username exists'
        )

    users[data.email] = data

    return {
        'message': 'user successfully registered!'
    }


@user_router.post('/signin')
async def sign_user_in(user: UserSignIn) -> dict:

    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )

    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='wrong credentials passed'
        )

    return {
        'message': 'user signed in successfully'
    }