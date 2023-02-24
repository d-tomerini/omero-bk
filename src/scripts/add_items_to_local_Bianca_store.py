# -*- coding: utf-8 -*-
"""
This programs connect to the local database to insert all the items
within the 'Data/all.csv' file.
It first drops the table before inserting the new data
"""

import pandas as pd

import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
models.BiancaLocalStore.__table__.drop(engine)
models.Base.metadata.create_all(bind=engine)


df = pd.read_csv('Data/all.csv')
df['BatchStart'] = pd.to_datetime(df.BatchStart)
df['BatchEnd'] = pd.to_datetime(df.BatchEnd)
records = df.to_dict(orient='records')

db = SessionLocal()
for r in records:
    db.add(models.BiancaLocalStore(**r))
db.commit()
