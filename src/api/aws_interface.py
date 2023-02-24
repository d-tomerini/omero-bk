# -*- coding: utf-8 -*-
"""
This is to connect to Bianca landing zone, query and retrieve data
"""

import os
import time

import boto3
from botocore.exceptions import ClientError

import exceptions
from api.secrets.tokens import (AWS_CATALOG, AWS_REGION, DATABASE_TABLE,
                                GLUE_CATALOG)


def wrangle_query_into_records(results_iterator):
    """
    Gets a paginated list result from a athena query,
    glue it together, specifically the get_query_result method used below.
    The query results populates a pandas dataframe.
    """

    table = []
    for results_page in results_iterator:
        for row in results_page['ResultSet']['Rows']:
            table.append(row['Data'])
    raw_schema = table.pop(0)
    schema = [val for item in raw_schema for val in item.values()]
    records = [{k: v.get('VarCharValue', None)
                for k, v in zip(schema, row)} for row in table]

    # This was a previous attempt to return a dataframe, from schema
    # records = [tuple(val for k in item for val in k.values()) for item in table]
    # df = pd.DataFrame.from_records(records, columns=schema)
    # return df
    return records


def get_athena_query_status(
        client,
        QueryExecutionId,
        max_retries=5,
        waiting=0.1):
    """
    Retries to get the status of the query with exponential backoff
    """
    t = 0
    retry = 0
    while retry < max_retries:
        r = client.get_query_execution(QueryExecutionId=QueryExecutionId)
        if 'QueryExecution' in r:
            state = r['QueryExecution']['Status']['State']
            if state == 'FAILED':
                raise Exception(
                    f'query with query id {QueryExecutionId} returned a status FAILED, {r}')
            if state == 'SUCCEEDED':
                print(f'got it after {retry} try and after {waiting} s ')
                return True
            time.sleep(waiting)
            t += waiting
            retry += 1
            waiting *= 2
            t += waiting
    raise Exception(
        f'Query id {QueryExecutionId} did not finish executing after {retry} tentatives and {t} seconds')


def get_athena_table(query):
    """
    Generate a query for athena filter
    NOTE: unfortunately key and value need a different quote (" vs ')
    """
    client = boto3.client(
        'athena',
        region_name=AWS_REGION
    )

    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': GLUE_CATALOG},
        ResultConfiguration={
            'OutputLocation': 's3://rnd-s3-athenaresults-bdsi-biancatoma'}
    )
    get_athena_query_status(
        client,
        response['QueryExecutionId'],
        max_retries=5,
        waiting=0.1
    )
    results_paginator = client.get_paginator('get_query_results')
    results_iterator = results_paginator.paginate(
        QueryExecutionId=response['QueryExecutionId'],
        PaginationConfig={
            'PageSize': 1000
        }
    )
    return wrangle_query_into_records(results_iterator)


def get_athena_schema():
    """
    Query the athena catalog to return the schema.
    It does not matter how it is defined, it will be lowercase!
    """
    client = boto3.client(
        'athena',
        region_name=AWS_REGION
    )

    response = client.get_table_metadata(
        CatalogName=aws_catalog,
        DatabaseName=GLUE_CATALOG,
        TableName=DATABASE_TABLE
    )
    cols = response['TableMetadata']['Columns']
    return [col['Name'] for col in cols]


def upload_to_s3(files, bucket):
    """
    upload the files to the landing zone bucket, to the specified hardcoded region.
    Might be better to create the client outside and pass it, for generality.
    """
    messages = []
    s3_client = boto3.client(
        's3',
        region_name=AWS_REGION
    )
    for file in files:
        try:
            s3_client.upload_fileobj(
                file.file,
                bucket,
                f'raw/{file.filename}')
        except ClientError as e:
            raise exceptions.upload_to_s3_failed(e)
        messages.append(
            f"Uploaded file {file.filename} successfully to {f'raw/{file.filename}'} in {bucket}.")
    return messages
