# -*- coding: utf-8 -*-
"""
Here we define the tokens, or take them from environment variables
"""

import os

# CENTREE_TOKEN = <value>
# tetrascience_token = <value>

CENTREE_TOKEN = os.getenv('CENTREE_TOKEN')
TETRASCIENCE_TOKEN = os.getenv('TETRASCIENCE_TOKEN')

# AWS catalog
AWS_CATALOG = 'AwsDataCatalog'
GLUE_CATALOG = 'rnd-glue-metadata-bdsi-biancatoma'
DATABASE_TABLE = 'rndbdsimetadatalocation'
AWS_REGION = os.getenv('AWS_REGION')
AWS_s3_LANDINGZONE = 'rnd-s3-cleanzone-bdsi-biancatoma'
