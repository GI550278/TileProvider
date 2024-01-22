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


@app.get("/")
def read_root():
    return {"Hello": config.params.source}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# @app.get("/shumar_v1/tileset.json")
@app.get("/shumar_v1")
def tileset_shumar_v1():
    file_path = r'C:\Users\sguya\PycharmProjects\TileProvider\storage\shumar_v1\tileset.json'
    path = pathlib.Path(file_path)
    last_modified = path.stat().st_mtime

    with open(file_path, 'r') as f:
        content = json.load(f)

    output_content = zlib.compress(json.dumps(content).encode('utf8'))

    headers = {
        "Last-Modified": make_http_time_string(last_modified),
        "Accept-Ranges": "bytes",
        "Cache-Control": "public, max-age=0",
        "Content-Type": "application/json",
        "Vary": "Accept-Encoding",
        "Content-Encoding": "deflate",
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=5",
        "Transfer-Encoding": "chunked",
        "Access-Control-Allow-Origin": "http://localhost:8083"
    }
    return Response(content=output_content, headers=headers)


@app.get("/3dtiles/{dir:str}/{file_path:path}")
async def read_file(dir: str, file_path: str):
    p = pathlib.Path(os.path.join(rf'C:\Users\sguya\PycharmProjects\TileProvider\storage\data\{dir}', file_path))
    if p.exists():
        last_modified = p.stat().st_mtime
        headers = {
            "Last-Modified": make_http_time_string(last_modified),
            "Access-Control-Allow-Origin": "http://localhost:8083"
        }
        return FileResponse(str(p), headers=headers)
    else:
        print(p)
        headers = {
            "Access-Control-Allow-Origin": "http://localhost:8083"
        }

        return Response(status_code=404, headers=headers)


"""
Request URL:
http://localhost:8083/public/shumar_v1/Buildings/B3DM/withTrees_26without_real_0_0_3_3_3.b3dm
Request Method:
GET
Status Code:
200 OK
Remote Address:
127.0.0.1:8083
Referrer Policy:
strict-origin-when-cross-origin

HTTP/1.1 200 OK
X-Powered-By: Express
Accept-Ranges: bytes
Date: Sun, 21 Jan 2024 08:29:53 GMT
Cache-Control: public, max-age=0
Last-Modified: Tue, 19 Dec 2023 12:55:47 GMT
ETag: W/"1b2684-1960022487"
Content-Type: application/octet-stream
Content-Length: 1779332
Connection: keep-alive
Keep-Alive: timeout=5


"""

"""
tileset

HTTP/1.1 200 OK
X-Powered-By: Express
Accept-Ranges: bytes
Date: Sun, 21 Jan 2024 08:26:11 GMT
Cache-Control: public, max-age=0
Last-Modified: Tue, 19 Dec 2023 13:29:59 GMT
ETag: W/"681-4144344686"
Content-Type: application/json
Vary: Accept-Encoding
Content-Encoding: deflate
Connection: keep-alive
Keep-Alive: timeout=5
Transfer-Encoding: chunked

"""
