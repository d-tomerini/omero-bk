# -*- coding: utf-8 -*-
# from fastapi.security import OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# from jose import jwt
import crud
import exceptions
import models
import schemas
from core.config import BASE_PATH
from database import get_db

router = APIRouter(
    prefix=f'{BASE_PATH}/stores',
    tags=['stores']
)


@router.get('/')
async def all_stores(db: Session = Depends(get_db)) -> List[schemas.StoreInfo]:
    """
    This provides a list of possible stores where to query the info.
    It will provide a list of the databases to search to get files
    """
    db_stores = crud.list_stores(db)
    stores = [schemas.StoreInfo.from_orm(s) for s in db_stores]
    return stores


@router.post('/add/')
async def add_stores(
        store: schemas.StoreInfo,
        db: Session = Depends(get_db)):
    """
    Convenience endpoint to add all a stores
    to the store databases.
    """
    item = crud.create_store(db, store)
    return {
        'message': f'Store {store.name} created',
        'store': schemas.StoreInfo.from_orm(item)
    }


@router.get('/schema/{store_name}')
async def get_schemas(
        store_name: str,
        db: Session = Depends(get_db)) -> schemas.ReturnedSchema:
    """
    Return the schema of the selected database

    """
    db_store = crud.get_store_by_name(db, store_name)
    if not db_store:
        raise exceptions.store_does_not_exist()
    store = schemas.StoreInfo.from_orm(db_store)
    schema = models.schema_from_tablename(store.name)
    if not schema:
        raise exceptions.table_not_set(store.name)
    return {
        'store': store,
        'database_schema': schema
    }
