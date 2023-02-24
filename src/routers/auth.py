# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

# import exceptions
# import crud
import schemas
from core.config import BASE_PATH

# from authorizations import SECRET_KEY, ALGORITHM
# from database import get_db


router = APIRouter(
    prefix=f'{BASE_PATH}/auth',
    tags=['auth']
)


@router.get('/login')
async def login() -> schemas.Message:
    """
    This will be the place to get an authentication token, when we decide
    how to implement it. Here just as a placeholder.
    The other methods will have to be update to support token exchange.
    """
    return {'message': 'This will return a JSW token'}
