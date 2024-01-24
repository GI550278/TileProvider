import json
import os
import pathlib
import sys
from datetime import datetime

from typing import Union

import yaml
from fastapi import FastAPI
from starlette.responses import JSONResponse, Response, FileResponse
import zlib
import time
from src.Config import config

app = FastAPI()


def make_http_time_string(timestamp):
    '''Input timestamp and output HTTP header-type time string'''
    time = datetime.fromtimestamp(timestamp)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT')


@app.get("/3dtiles/{source:int}/{file_path:path}")
async def read_file(source: int, file_path: str):
    if 0 <= source < len(config.params['sources']):
        directory = config.params['sources'][source]
    else:
        return Response(status_code=404, headers={
            "Access-Control-Allow-Origin": config.params['sources']['Allow-Origin']
        })

    p = pathlib.Path(os.path.join(directory, file_path))
    if p.exists():
        last_modified = p.stat().st_mtime
        headers = {
            "Last-Modified": make_http_time_string(last_modified),
            "Access-Control-Allow-Origin": config.params['Allow-Origin']
        }
        return FileResponse(str(p), headers=headers)
    else:
        return Response(status_code=404, headers={
            "Access-Control-Allow-Origin": config.params['Allow-Origin']
        })


@app.head("/3dtiles/{source:int}/{file_path:path}")
async def is_exist(source: int, file_path: str):
    if 0 <= source < len(config.params['sources']):
        directory = config.params['sources'][source]
    else:
        return Response(status_code=404, headers={
            "Access-Control-Allow-Origin": config.params['sources']['Allow-Origin']
        })

    p = pathlib.Path(os.path.join(directory, file_path))
    if p.exists():
        last_modified = p.stat().st_mtime
        headers = {
            "Last-Modified": make_http_time_string(last_modified),
            "Access-Control-Allow-Origin": config.params['Allow-Origin']
        }
        return Response(str(p), headers=headers)
    else:
        return Response(status_code=404, headers={
            "Access-Control-Allow-Origin": config.params['Allow-Origin']
        })
