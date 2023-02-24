# -*- coding: utf-8 -*-
"""
fastapi exceptions for convenience
"""

from fastapi import HTTPException, status


def store_does_not_exist():
    """ store does not exist in database list"""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Store does not exist'
    )


def table_not_set(store_name):
    """ trying to set value to a table that does not have a model """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Table for metadata store {store_name} not set up properly in Database')


def upload_to_s3_failed(error):
    """ upload to s3 of one of the files failed """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f'Upload to s3 failed: {error}'
    )
