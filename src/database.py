# -*- coding: utf-8 -*-
# database details
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'sqlite:////mnt/bdsi.db'

if os.getenv('DOMINO_WORKING_DIR'):
    HOME = os.getenv('DOMINO_WORKING_DIR')
else:
    HOME = os.getenv('HOME')

SQLALCHEMY_DATABASE_URL = f'sqlite:////mnt/bdsi.db' # rstudio
# SQLALCHEMY_DATABASE_URL = f'sqlite:///{HOME}/datalake-backend/bdsi.db' # rstudio
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/dbsi.db" #eventually, on production


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False
    }
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
