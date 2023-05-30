import http.client
import imp
import os
import sys
from urllib import parse


EXTENTION = ".txt"


def _create_full_path(path: str, fullname: str) -> str:
    """インターネットへのパスを生成するヘルパー関数"""
    url_component = parse.urlparse(path)
    target = (
        url_component.scheme
        + "://"
        + url_component.netloc
        + os.path.join(os.path.normpath(url_component.path), *(fullname.split(".")))
        + EXTENTION
    )
    return target


def _package_path(path: str, fullname: str) -> str:
    """インターネットのパッケージパスを生成するヘルパー関数"""
    target = _create_full_path(path, fullname)
    res = os.path.dirname(target) + f"/{fullname}/__init__" + EXTENTION
    return res


def _exist_url(target) -> bool:
    """指定されたパスがインターネット上に存在するか確認するヘルパー関数"""
    url_component = parse.urlparse(target)
    conn = http.client.HTTPConnection(url_component.netloc)
    conn.request("HEAD", url_component.path)
    res = conn.getresponse()
    if __debug__:
        print(f"{res.status}: {target}")
    if 200 <= res.status < 400:
        return True
    return False
