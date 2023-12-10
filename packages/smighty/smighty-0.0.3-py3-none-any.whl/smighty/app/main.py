# Copyright 2023 Weavers @ Eternal Loom. All rights reserved.
#
# Use of this software is governed by the license that can be
# found in LICENSE file in the source repository.

# The main API app entry point for Smighty

import logging
from typing import Annotated, Any

from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse

from .consts import APP_INITIALIZED_MESSAGE, APP_INITIALIZED_MESSAGE_HTML

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/', tags=['root'])
async def root(accept: Annotated[str, Header()]) -> Any:
    """Root context of the Application"""

    # Poorman's templating
    # accept = request.headers['accept'].split(',')[0]
    accept = accept.split(',')[0]
    logging.info(f'Accept: {accept}')
    if accept == 'text/html':
        return HTMLResponse(content=APP_INITIALIZED_MESSAGE_HTML, status_code=200)
    else:
        return {'message': APP_INITIALIZED_MESSAGE}
