# -*- coding: utf-8 -*-
# this is for postgres database. Not supported by sqlite3, older version
from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

import schemas
from api.aws_interface import get_athena_schema
from database import Base


class StoreInfo(Base):
    """ Model for a store"""
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    label = Column(String)
    local = Column(String)
    online = Column(String)


class BiancaLocalStore(Base):
    """ Model for the store"""
    __tablename__ = 'local_store'
    table_id = Column('id', Integer, primary_key=True, index=True)
    project_name = Column('ProjectName', String)
    compound = Column('Compound', String)
    experimental_system = Column('ExperimentalSystem', String)
    therapeutic_area = Column('TherapeuticArea', String)
    disease = Column('Disease', String)
    data_type = Column('Data Type', String)
    operator_name = Column('OperatorName', String)
    samples = Column('Samples', String)
    batch_id = Column('BatchID', String)
    batch_start = Column('BatchStart', DateTime)
    batch_end = Column('BatchEnd', DateTime)
    instrument_type = Column('InstrumentType', String)
    metadata_file_name = Column('MetadataFileName', String)
    raw_file_name = Column('RawFileName', String)
    s3_bucket_name = Column('S3BucketName', String)
    raw_file_uri = Column('RawFileURI', String)
    arn_raw_file = Column('ArnRawFile', String)


class TetrascienceLocal(Base):
    """ Database model for a tetrascience query"""
    __tablename__ = 'tetrascience_local'
    table_id = Column('id', Integer, primary_key=True, index=True)
    uuid = Column('fileId', String)
    raw_file_id = Column('rawFileId', String)
    file_path = Column('filePath', String)
    tags = Column(String)  # should be json
    trace_id = Column('traceId', String)
    source = Column(String)
    site = Column('Site', String)
    department = Column('Department', String)
    organisation = Column('Organisation', String)
    instrument_name = Column('Instrument Name', String)
    instrument_type = Column('Instrument type', String)
    time_column = Column('Time', String)
    date_column = Column('Date', String)
    location = Column('Location', String)
    serial_number = Column('Serial Number', String)


class MetadataFields(Base):
    """
    Database containing the fields required/optional to upload.
    At the moment it is a bit experimental, deserves thinking more
    about the model structure."""
    __tablename__ = 'metadata_fields'
    table_id = Column('id', Integer, primary_key=True, index=True)
    store = Column(String, nullable=False)
    field_name = Column(String, nullable=False)
    required = Column(Boolean, nullable=False)
    autogenerated = Column(Boolean, nullable=False)
    searchable = Column(String)
    search_list = Column(String)
    content_type = Column(String, nullable=False)
    centree_name = Column(String)
    centree_ontology = Column(String)


class ImageTest(Base):
    """
    Upload for images. Mainly to test the desired functionality
    from the upload, text type and such
    """
    __tablename__ = 'image_test'
    table_id = Column('id', Integer, primary_key=True, index=True)
    image_path = Column('Image path', String)
    channel_information = Column('Channel Information', String)
    dimension = Column('Dimension', String)
    image_format = Column('Format', String)
    modality = Column('Modality', String)
    instrument = Column('Instrument', String)
    image_id = Column('Image ID', String)
    sex = Column('Sex', String)
    age_unit = Column('Age Unit', String)
    sample_id = Column('Sample ID', String)
    author = Column('Author', String)
    uploaded_by = Column('Uploaded By', String)
    acquired_by = Column('Acquired By', String)
    dataset_name = Column('Dataset Name', String)
    project_description = Column('Project Description', String)
    project_id = Column('Project ID', String)
    project_name = Column('Project Name', String)
    site = Column('Site', String)
    country = Column('Country', String)
    team = Column('Team', String)
    division = Column('Division', String)
    dataset_id = Column('Dataset ID', String)
    date_acquired = Column('Date Acquired', String)
    acquired_from = Column('Acquired From', String)
    source = Column('Source', String)
    image_type = Column('Type', String)
    species = Column('Species', String)
    biological_entity = Column('Biological Entity', String)
    experimental_group = Column('Experimental Group', String)
    age = Column('Age', Integer)


def table_from_local_database(store):
    """
    Choose a sqlalchemy model WRT the local tables
    """
    available_tables = {
        'BDSI': BiancaLocalStore,
        'TetraScience': TetrascienceLocal,
        'ImageTest': ImageTest
    }

    return available_tables.get(store, None)


def schema_from_tablename(store):
    """
    Convenience function to return the schema of the table.
    It either gets it from the local store, or athena.
    Ad hoc solution
    """
    if store == 'AWS':
        return get_athena_schema()
    table = table_from_local_database(store)
    if not table:
        return None
    return [col.name for col in table.__table__.columns]
