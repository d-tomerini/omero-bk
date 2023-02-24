# -*- coding: utf-8 -*-
"""
This programs connect to the local database to insert all the items
within the 'Data/all.csv' file.
It first drops the table before inserting the new data
"""

import json

import pandas as pd

import models
import schemas
from database import SessionLocal, engine

models.TetrascienceLocal.__table__.drop(engine)
models.Base.metadata.create_all(bind=engine)


df = pd.read_csv('Data/DFTetrascience-metadata.csv')
df['tags'] = df['tags'].str.replace("'", '"')
# df['tags'] = df['tags'].apply(lambda x: json.loads(x))

records = df.to_dict(orient='records')

con = engine.connect()
df.to_sql('tetrascience_local', con, if_exists='append', index=False)
