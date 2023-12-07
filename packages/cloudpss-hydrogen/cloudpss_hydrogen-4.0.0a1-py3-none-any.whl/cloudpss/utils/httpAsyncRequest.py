import json
import os
from aiohttp import ClientSession, WSMsgType
from urllib.parse import urljoin
import logging
from ..version import __version__


def graphql_version_check(uri, response):
    if uri.startswith("graphql"):
        if "X-Cloudpss-Version" not in response.headers:
            raise Exception("当前SDK版本（ver 3.X.X）与服务器版本（3.0.0 以下）不兼容，请更换服务器地址或更换SDK版本。")
        os.environ["X_CLOUDPSS_VERSION"] = response.headers["X-Cloudpss-Version"]
        if float(response.headers["X-Cloudpss-Version"]) >= 5:
            raise Exception(
                "当前SDK版本（ver "
                + __version__
                + "）与服务器版本（ver "
                + response.headers["X-Cloudpss-Version"]
                + ".X.X）不兼容，请更换服务器地址或更换SDK版本(pip 使用 pip install -U cloudpss 命令更新, conda 使用 conda update cloudpss 命令更新)。"
            )


### 通过aiohttp实现请求
async def fetch_data(method: str, uri, data, baseUrl=None, params={}, **kwargs):
    if baseUrl == None:
        baseUrl = os.environ.get("CLOUDPSS_API_URL", "https://cloudpss.net/")
    url = urljoin(baseUrl, uri)
    token = os.environ.get("CLOUDPSS_TOKEN", None)
    if token:
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json; charset=utf-8",
        }
    else:
        raise Exception("token undefined")
    logging.debug("fetch start:")
    async with ClientSession() as session:
        async with session.request(
            method, url, data=data, params=params, headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                logging.debug("data:")
                logging.debug(data)
                logging.debug("params:")
                logging.debug(params)
                graphql_version_check(uri, response)
                # if "statusCode" in r.text:
                #     t = json.loads(r.text)
                #     raise  Exception(str(t['statusCode']) + " "+t['message'])
                return data
            elif 400 <= response.status < 500:
                raise Exception(f"请求失败，状态码：{response.status}")
            elif 500 <= response.status < 600:
                raise Exception(f"请求失败，状态码：{response.status}")
            else:
                return


# graphql实现方法
async def graphql_fetch(query, variables=None):
    payload = {"query": query, "variables": variables}
    return await fetch_data("POST", "graphql", data=json.dumps(payload))


# websocket
async def websocket_connect(url, open_func, receive_func, closed_func, error_func):
    async with ClientSession() as session:
        async with session.ws_connect(url) as ws:
            # ws.register_callback("connecting", lambda: logging.debug("连接正在建立..."))
            # ws.register_callback("connected", lambda: open_func())
            # ws.register_callback("closed", lambda: closed_func())
            # ws.register_callback("error", lambda: error_func())
            open_func()
            async for msg in ws:
                
                if msg.type == WSMsgType.BINARY:
                    receive_func(msg.data)
                if msg.type == WSMsgType.TEXT:
                    receive_func(msg.data)
                elif msg.type == WSMsgType.CLOSED:
                    logging.debug("WebSocket连接已关闭")
                    closed_func()
                    break
                elif msg.type == WSMsgType.ERROR:
                    logging.debug(f"WebSocket连接发生错误：{msg.data}")
                    error_func(msg.data)
                    break
