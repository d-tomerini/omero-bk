# -*- coding: utf-8 -*-

title = 'Back-end API for the datalake landing zone'
description = """
This API set is meant to use as a back-end for the landing zone of data.
It provides the searchable metadata tables, search queries, and metadata fields to upload.
"""
project_version = '0.1'
contact = {
    'name': ' I&T',
    'email': 'daniele.tomerini@cslbehring.com',
}

BASE_PATH = '/api/v1'

settings = dict(
    title=title,
    description=description,
    project_version=project_version,
    contact=contact
)

tags_metadata = [{'name': 'auth',
                  'description': 'Not implemented. All the things related to authentication, tokens, login will go here.'},
                 {'name': 'search',
                  'description': 'Endpoints dealing with searching, creating, deleting the database containing metadata information.'},
                 {'name': 'stores',
                  'description': 'Information about the metadata stores, and where to connect to get the data.'}]
