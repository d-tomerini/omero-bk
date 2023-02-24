# -*- coding: utf-8 -*-
"""
This programs connect to the local database to insert all the items
within the 'Data/all.csv' file.
It first drops the table before inserting the new data.
"""

import pandas as pd

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
models.MetadataFields.__table__.drop(engine)
models.Base.metadata.create_all(bind=engine)


df = pd.read_json('Data/fields.json', orient='records')
records = df.to_dict(orient='records')

meta_records = [schemas.MetadataFieldsIn(**r) for r in records]
db = SessionLocal()
for r in meta_records:
    db.add(models.MetadataFields(**dict(r)))
db.commit()
