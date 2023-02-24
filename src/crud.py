# -*- coding: utf-8 -*-
# database utils
# save, read and update local info

from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas


def create_store(db: Session, store: schemas.StoreInfo):
    db_store = models.StoreInfo(**dict(store))
    db.add(db_store)
    db.commit()
    return db_store


def list_stores(db: Session):
    return db.query(models.StoreInfo).all()


def get_store_by_name(db: Session, store_name):
    db_store = db.query(
        models.StoreInfo).filter(
        models.StoreInfo.name == store_name)
    return db_store.first()


def get_fields_by_store(db: Session, store_name):
    db_fields = db.query(
        models.MetadataFields).filter(
        models.MetadataFields.store == store_name)
    return db_fields.all()
