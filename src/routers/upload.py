# -*- coding: utf-8 -*-
import base64
import os
# from fastapi.security import OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

# from jose import jwt
import crud
import exceptions
import models
import schemas
from api.aws_interface import upload_to_s3
from api.secrets.tokens import AWS_REGION, AWS_s3_LANDINGZONE
from core.config import BASE_PATH
from database import get_db

router = APIRouter(
    prefix=f'{BASE_PATH}/upload',
    tags=['upload']
)


@router.get('/{store_name}/fields')
async def get_fields(
    store_name: str,
    db: Session = Depends(get_db)
):
    """
    This endpoint runs a validation of fields to be uploaded
    with respect to the stored schema
    """
    db_store = crud.get_store_by_name(db, store_name)
    if not db_store:
        raise exceptions.store_does_not_exist()
    db_fields = crud.get_fields_by_store(db, store_name)
    fields = [schemas.MetadataFieldsOut.from_orm(s) for s in db_fields]
    return {
        'store': store_name,
        'fields': fields
    }


@router.post('/{store}/validate')
async def validate_fields():
    """
    This endpoint runs a validation of fields to be uploaded
    with respect to the stored schema
    """
    return {'message': 'Hello verification'}


@router.post('/{store}/to_landing_zone')
async def upload_test(
        store,
        files: List[UploadFile],
        db: Session = Depends(get_db)):
    """
    This endpoint uploads a file to the relevant metadata store.
    It does not check or validate anything.
    """
    db_store = crud.get_store_by_name(db, store)
    if not db_store:
        raise exceptions.store_does_not_exist()
    if store == 'AWS':
        messages = upload_to_s3(files, AWS_s3_LANDINGZONE)
    else:
        table = models.table_from_local_database(store)
        if not table:
            raise exceptions.table_not_set()
        # do something locally with the files;
        # here I only update the store table with the info

    return {
        'message': messages,
        'filenames': [
            file.filename for file in files]}
