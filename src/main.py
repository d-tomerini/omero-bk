# -*- coding: utf-8 -*-
import os

import uvicorn
from fastapi import FastAPI

import models
import schemas
from core.config import BASE_PATH, settings, tags_metadata
from database import engine
from routers import auth, search, stores, upload

app = FastAPI(
    **settings,
    openapi_tags=tags_metadata,
    openapi_url='/openapi.json',
    docs_url='/docs'
)

models.Base.metadata.create_all(bind=engine)

DOMINO_SLUG = 'https://domino-qa-us.cda.cslbehring.com'
USER = os.environ.get('DOMINO_PROJECT_OWNER')
PROJECT = os.environ.get('DOMINO_PROJECT_NAME')
RUNID = os.environ.get('DOMINO_RUN_ID')
BASE_PATH = f'{USER}/{PROJECT}/r/notebookSession/{RUNID}/api/v1' if USER else '/api/v1'
RUNURL = f'{DOMINO_SLUG}/{BASE_PATH}'
HOSTNAME = os.environ.get('HOSTNAME')
FASTAPI_PORT = int(os.environ.get('FASTAPI_PORT')
                   ) if os.environ.get('DASH_PORT') else 8888


@app.get(f'/')
async def root() -> schemas.Message:
    """
    This is a compromise solution to be analyzed further.
    Domino standard app does *not* allow serving app on URLs that have routes or params;
    furthermore, the json response is embedded in javascript and html code.

    There are three further addressess that serves the app: two are headless, and are adequate for
    the functionality I need. Problems:
      - one `https://https://domino.cslg1.cslg.net/{user_id}/{projet_name}/app` is static, but does not provide
        access to html routes;
      - the third option does provide access to routes, but its location dynamically changes
        upon each server restart with info about the session (e.g., its address cannot be stored by the backend).

    I provide two solutions:
      - the "/" route contains the dynamic app address, that can be used in further calls;
      - the ```https://https://domino.cslg1.cslg.net/{user_id}/{projet_name}/app``` provides a `307` redirect
        to the desired addresses. In particular, the address is returned in the `response.url`
        attribute of the python `response` package allows routes, but is dynamically generated at runs.

    More information at the domino page:

    `https://tickets.dominodatalab.com/hc/en-us/articles/10014367822612-App-URLs-and-URL-parameters`.

    """

    if USER:
        return {'message': RUNURL}
    else:
        return {'message': f'{HOSTNAME}:{FASTAPI_PORT}/api/v1/'}

app.include_router(auth.router)
app.include_router(search.router)
app.include_router(upload.router)
app.include_router(stores.router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=FASTAPI_PORT,
        reload=True,
    )
