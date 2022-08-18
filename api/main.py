from random import random
import logging,logging.config
import random
import string
import uvicorn
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import FastAPI
from functions.get_today_weather_param import get_today_weather_param
from functions.save_params_into_db import save_params_into_db

logging.config.fileConfig('log/logging.conf')
logger = logging.getLogger(__name__)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


users_db = {

    "yijun": {
        "username": "yijun",
        "full_name": "yijun",
        "email": "yijun@example.com",
        "hashed_password": "$2b$12$d3/0FX35PD6KE7xXNAYtl.XEPZQf3dXZp6cINNXctetqbauvQ44BS",
        "disabled": False,
    },
    "zhijie": {
        "username": "zhijie",
        "full_name": "zhijie",
        "email": "zhijie@example.com",
        "hashed_password": "$2b$12$wyGrJ9ddK5rEDr/8TOD9TOxB./KimH1HhJdsmKJZ50qGClc0xnhze",
        "disabled": False,
    },
    "team4": {
        "username": "team4",
        "full_name": "team4",
        "email": "team4@example.com",
        "hashed_password": "$2b$12$coUIbxzhTrGdVxy4SsZ32.c8znlZ58I4wiC/Qw0xHuYq6D4FXZjxi",
        "disabled": False,
    },
    "parth": {
        "username": "parth",
        "full_name": "parth",
        "email": "parth@example.com",
        "hashed_password": "$2b$12$D8MCfcRSPwoVFGo9QTdE0ODBX25cMyOHh/HFEMJI4adNzUVJNOwvS",
        "disabled": False,
    },
    "srikanth": {
        "username": "srikanth",
        "full_name": "srikanth",
        "email": "srikanth@example.com",
        "hashed_password": "$2b$12$Ky4RCizJYaL1tCx1X0MeVuAoIWXPO.YRLDKEexQbhYOPqnYLR6KX6",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get('/')
async def welcome():
    return {"Team3": "Welcome to Lookout APi on Docker"}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]

@app.middleware("http")
async def log_requests(request: Request, call_next):
   idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
   
   logger.info(f"{request.url.path}")
   #start_time = time.time()
   response = await call_next(request) 
   #process_time = (time.time() - start_time) * 1000
   return response;


@app.get("/today/weather")
async def Load_today_weather_params():
    result = get_today_weather_param()
    # logger.info(f"User {current_user.username} load current weather data at {tdatetime}")
    
    return result;


@app.post("/db/record/today")
async def Store_today_weather(key_id: str, tdatetime: str, precipitation: str, 
                    temp_max: str, temp_min: str, wind: str, real_weather: str,
                    
                    ):
    try:
        save_params_into_db(key_id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather)
    except Exception as e:
        logger.error(f"Failed to save weather data at {tdatetime}")
        print(e)
        return {"error": "Failed to saving weather record"}

    # logger.info(f"User {current_user.username} save weather data at {tdatetime}")  

# @app.get("/db/record")
# async def Store_today_weather(current_user: User = Depends(get_current_active_user)):

#     return 

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)