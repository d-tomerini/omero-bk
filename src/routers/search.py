# -*- coding: utf-8 -*-
"""
Router deals with database search.
Return results from one of the allowed stores.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
import exceptions
import models
import schemas
from api.aws_interface import get_athena_table
from api.secrets.tokens import DATABASE_TABLE, GLUE_CATALOG
from core.config import BASE_PATH
from database import get_db

# from fastapi.security import OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
# from typing import Optional
# from jose import jwt



router = APIRouter(
    prefix=f'{BASE_PATH}/search',
    tags=['search']
)


@router.get('/{store_name}')
async def search(
        store_name: str,
        q: str = '',
        offset: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)) -> schemas.SearchRows:
    """
    Main function to return a database search.
    Returned info will depend on the queried database.
    :param store_name: one of the available databases, listed on the /stores/ endpoint
    :param q: query key with the SQL query string
    :param offset: which row to start from, for pagination
    :param limit: how many rows to return
    TODO check the ORDER BY in AWS, missing ID.
         Will definitely have a unique key in the future
    """
    db_store = crud.get_store_by_name(db, store_name)
    if not db_store:
        raise exceptions.store_does_not_exist()
    store = schemas.StoreInfo.from_orm(db_store)
    if store.name == 'AWS':
        paginate = f'ORDER BY "Compound"  OFFSET {offset} LIMIT {limit}'
        query = f'SELECT * FROM "{GLUE_CATALOG}"."{DATABASE_TABLE}" {q} {paginate}'
        count_query =  f'SELECT COUNT(*) FROM "{GLUE_CATALOG}"."{DATABASE_TABLE}" {q}'
    if store.local:
        table = models.table_from_local_database(store.name)
        if not table:
            raise exceptions.table_not_set(store.name)
        paginate = f'ORDER BY "id" LIMIT {limit} OFFSET {offset}'
        query = f'SELECT * FROM {table.__tablename__} {q} {paginate}'
        count_query = f'SELECT COUNT(*) FROM {table.__tablename__} {q}'
    rows = execute_query(store, db, query)
    count_dict = execute_query(store, db, count_query)
    count =list(count_dict[0].values())[0]
    return schemas.SearchRows(
        store=store,
        count=count,
        items=rows)


@router.get('/{store_name}/distinct/{column}')
async def search_distinct(
        store_name: str,
        column: str,
        q: str = '',
        offset: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)) -> schemas.SearchRows:
    """
    To return distinct values to fill the search page.
    Not sure it is better.
    Returned info will depend on the queried database.
    """
    db_store = crud.get_store_by_name(db, store_name)
    if not db_store:
        raise exceptions.store_does_not_exist()
    store = schemas.StoreInfo.from_orm(db_store)
    query = f'SELECT DISTINCT {column} FROM '
    count_query = f'SELECT COUNT(DISTINCT {column}) FROM '
    if store.name == 'AWS':
        paginate = f'ORDER BY "{column}"  OFFSET {offset} LIMIT {limit}'
        query += f'"{GLUE_CATALOG}"."{DATABASE_TABLE}" {q} {paginate}'
        count_query =  f'{query} "{GLUE_CATALOG}"."{DATABASE_TABLE}" {q}'
    if store.local:
        table = models.table_from_local_database(store.name)
        if not table:
            raise exceptions.table_not_set(store.name)
        query += f'{table.__tablename__} {q} LIMIT {limit}'
        count_query =  f'{query} {table.__tablename__} {q}'
    rows = execute_query(store, db, query)
    count_dict = execute_query(store, db, count_query)
    count =list(count_dict[0].values())[0]
    items_list = [v for item in rows for v in item.values()]
    return schemas.SearchRows(
        store=store,
        count=count,
        items=items_list)


def execute_query(store, db, query):
    """
    Runs a generic query against one of the stores
    :param store: database to check
    :param db: connection session
    :param query: the query to run
    """
    if store.name == 'AWS':
        rows = get_athena_table(query)
    if store.local:
        db_rows = db.execute(query).fetchall()
        # sqlalchemy 1.3 rows = [{k:v for k,v in row.items()} for row in
        # db_rows]
        rows = [dict(row) for row in db_rows]
    return rows
