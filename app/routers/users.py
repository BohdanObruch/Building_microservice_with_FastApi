from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from app.database import users
from app.models.user import User, UserCreate, UserUpdate
from fastapi_pagination import Page, paginate
from pydantic import ValidationError


router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", status_code=HTTPStatus.OK, response_model=Page[User])
def get_users() -> Page[User]:
    return paginate(users.get_users())


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    try:
        UserCreate.model_validate(user.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=e.errors())

    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    try:
        UserUpdate.model_validate(user.model_dump())
    except ValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=e.errors())

    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")

    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    users.delete_user(user_id)
    return {"message": "User deleted"}
