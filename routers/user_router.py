from fastapi import APIRouter, status
from http import HTTPStatus

from fastapi.encoders import jsonable_encoder

from schemas import RegisterModel, LoginModel, UserPasswordResetModel, UserUpdateModel
from database import Session, ENGINE
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.exceptions import HTTPException


user_router = APIRouter(prefix="/user", tags=["user"])
session = Session(bind=ENGINE)


@user_router.get("/")
async def auth():
    return {"message": "Auth page"}


@user_router.get("/login")
async def login():
    return {"message": "Login page"}


@user_router.post("/login")
async def user_login(user: LoginModel):
    check_user = session.query(User).filter(User.username == user.username).first()
    if check_user is not None:
        if check_password_hash(check_user.password, user.password):
            return HTTPException(status_code=status.HTTP_200_OK, detail="Login successful")

        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.get("/register")
async def get_register():
    return {"message": "Register page"}


@user_router.post("/register", status_code=HTTPStatus.CREATED)
async def create_user(user: RegisterModel):
    check_username = session.query(User).filter(User.username == user.username).first()
    if check_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")


    check_email = session.query(User).filter(User.email == user.email).first()
    if check_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")



    new_user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED, detail="User created successfully")



# @user_router.get("/users")
# async def get_users():
#     users = session.query(User).all()
#     return users



@user_router.get("/users")
async def get_users():
    users = session.query(User).all()
    data = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password[-10:]
        }
        for user in users
    ]
    return jsonable_encoder(data)




@user_router.put("/change-password/{id}")
async def change_password(id: int, user: UserPasswordResetModel):
    check_user = session.query(User).filter(User.id == id).first()
    if check_user:
        if user.password == user.password_2:
            check_user.password = generate_password_hash(user.password)
            session.add(check_user)
            session.commit()
            data = {"message": "Password changed successfully"}
            return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.put("/users/{id}")
async def update_user(id: int, user: UserUpdateModel):
    check_user = session.query(User).filter(User.id == user.id).first()
    if check_user:
        for key, value in user.dict().items():
            setattr(check_user, key, value)

        data = {
            "code": 200,
            "message": "User updated successfully",
            "object": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "is_active": user.is_active,
                "is_staff": user.is_staff
            }
        }

        session.add(check_user)
        session.commit()
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.delete("/user/{id}")
async def delete_user(id: int):
    check_user = session.query(User).filter(User.id == id).first()
    if check_user:
        session.delete(check_user)
        session.commit()

        data = {"message": "User deleted successfully"}
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")