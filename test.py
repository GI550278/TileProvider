import os
import pathlib
import time
from datetime import datetime

file_path = r'C:\Users\sguya\PycharmProjects\TileProvider\storage\shumar_v1\tileset.json'
path = pathlib.Path(file_path)
last_modified = path.stat().st_mtime


def make_http_time_string(timestamp):
    '''Input timestamp and output HTTP header-type time string'''
    time = datetime.fromtimestamp(timestamp)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT')


#
# print(last_modified)
# t = fo.strftime('%a, %d %b %Y %H:%M:%S GMT')
# print(t)

dir = "Telem-Op-May16_Build_4_ppp"
file_path = "tileset.json"
p = pathlib.Path(os.path.join(rf'C:\Users\sguya\PycharmProjects\TileProvider\storage\data\{dir}', file_path))
print(p)
print(p.exists())

p = pathlib.Path(r'O:\Data')
print(p.exists())
print(os.path.exists(rf'C:\Users\sguya\PycharmProjects\TileProvider\storage\data\3DBest'))
