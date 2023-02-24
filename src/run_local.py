# -*- coding: utf-8 -*-
import os

import uvicorn

if __name__ == '__main__':
    dash_port = int(os.environ.get('DASH_PORT')
                    ) if os.environ.get('DASH_PORT') else 8889
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=dash_port,
        reload=True)
