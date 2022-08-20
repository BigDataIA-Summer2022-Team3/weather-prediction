from random import random
import logging,logging.config
import random
import string
import uvicorn
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import FastAPI
from functions.load_history_weather import load_history_weather
from functions.get_weather_in_5_days import get_weather_in_5_days
from functions.get_past_one_week_weather import get_past_one_week_weather
from functions.get_today_weather_param import get_today_weather_param
from functions.save_params_into_db import save_params_into_db
from functions.save_log_into_db import save_log_into_db

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


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/')
async def welcome():
    return {"Team3": "Welcome to weather overview!"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.middleware("http")
async def log_requests(request: Request, call_next):
   idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
   
   logger.info(f"{request.url.path}")
   response = await call_next(request) 
   return response;


@app.post("/db/record/today")
async def Store_today_weather(key_id: str, tdatetime: str, precipitation: str, 
                    temp_max: str, temp_min: str, wind: str, real_weather: str,
                    ):
    """
    This function will call save_params_into_db() function
    The function is used to upload daily meteorological data to MySQL.
    Function get key_id, datetime, precipitation, highest temp, lowest temp, wind and reall weather, 
        then use sql code to upload data to MySQL
    """
    try:
        save_params_into_db(key_id, tdatetime, precipitation, temp_max, temp_min, wind, real_weather)
        date = datetime.today() 
        inf = logger.info(f"username='airflow'; save today weather at {date}")
        save_log_into_db(f"username='airflow'; save today weather at {date}")
    except Exception as e:
        logger.error(f"Failed to save weather data at {tdatetime}")
        print(e)
        return {"error": "Failed to saving weather record"}

    logger.info(f"Airflow save weather data at {tdatetime}")  


@app.get("/today/weather")
async def Load_today_weather_params():
    """
    This function will call get_today_weather_param() function
    we set a timily dag in airflow, every day the dag will call this function to get the meteorological data from OpenAPI 
    """
    result = get_today_weather_param()
    date = datetime.today() 
    inf = logger.info(f"username='airflow'; Load_today_weather at {date}")
    save_log_into_db(f"username='airflow'; Load_today_weather at {date}")
    return result


@app.get("/last7days/weather")
async def Get_last_one_week_weather(current_user: User = Depends(get_current_active_user)):
    """
    This function will call get_past_one_week_weather() function
    The function will get past 7 days meteorological data from MySQL and return them
    user can use streamlit to call this function, and it will return last 7 days' precipitation, temp_max, temp_min, wind
    """
    try:
        date = datetime.today()
        fullstr = str(current_user)
        name = fullstr.split(' ')[0]
        logger.info(f"{name}; retrieve past one week weather at {date}")
        save_log_into_db(f"{name}; retrieve past one week weather at {date}")
        result = get_past_one_week_weather()
    except Exception as e:
        logger.warning(e)
    return result


@app.get("/predict/5days")
async def Get_and_Predict_weather_in_5_days(current_user: User = Depends(get_current_active_user)):
    """
    This function will call get_weather_in_5_days() function
    The function will get next 5 days meteorological data and analyze the weather, then return those meteorological data and weather
    """
    try:
        result = get_weather_in_5_days()
        date = datetime.today()
        fullstr = str(current_user)
        name = fullstr.split(' ')[0]
        inf = logger.info(f"{name}; get predicted weather in 5 days at {date}")
        save_log_into_db(f"{name}; get predicted weather in 5 days at {date}")
    except Exception as e:
        logger.warning(e)
    return result


@app.get("/history")
async def Load_history_weather_in_one_year(input_year:int, current_user: User = Depends(get_current_active_user)):
    """
    This function will call load_history_weather(), it need input an int as Year
    The function will search specified year in MySQL and return the year data as a dictionary
    """
    try:
        result = load_history_weather(input_year)
        date = datetime.today() 
        fullstr = str(current_user)
        name = fullstr.split(' ')[0]
        inf = logger.info(f"{name}; Load history weather in year {input_year} at {date}")
        save_log_into_db(f"{name}; Load history weather in year {input_year} at {date}")
    except Exception as e:
        logger.warning(e)
    return result

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)