from fastapi import HTTPException, status, APIRouter

from database.connection import Database
from models.users import UserSignIn, User

user_router = APIRouter(
    tags=['User']
)

user_database = Database(User)


@user_router.post('/signup')
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with supplied username exists'
        )
    else:
        await user_database.save(user)
        return {
            'message': 'user successfully registered!'
        }


@user_router.post('/signin')
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )

    if user_exist.password == user.password:
        return {
            'message': 'user signed in successfully'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='wrong credentials passed'
        )

