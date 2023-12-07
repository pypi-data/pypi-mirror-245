#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2023/5/26 09:23
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://geek-docs.com/fastapi/fastapi-questions/279_fastapi_uvicorn_python_run_both_http_and_https.html
# 请求限制 https://github.com/Unstructured-IO/pipeline-paddleocr/blob/main/prepline_paddleocr/api/paddleocr.py
# todo: 增加apikey、增加调用频次

from meutils.pipe import *
from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware

from meutils.serving.fastapi.exceptions.http_error import http_error_handler
from meutils.serving.fastapi.exceptions.validation_error import http422_error_handler


class App(FastAPI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
        self.add_exception_handler(HTTPException, http_error_handler)
        self.add_exception_handler(RequestValidationError, http422_error_handler)

    def include_router(self, router, prefix='', **kwargs):
        """
            from fastapi import FastAPI, APIRouter
            router = APIRouter(route_class=LoggingRoute)

        :param router:
        :param prefix:
        :param kwargs:
        :return:
        """

        super().include_router(router, prefix=prefix, **kwargs)

    def run(self, app=None, host="0.0.0.0", port=8000, workers=1, access_log=True, reload=False, **kwargs):
        """

        :param app:
            f"{Path(__file__).stem}:{app}"
            app字符串可开启热更新 reload
        :param host:
        :param port:
        :param workers:
        :param access_log:
        :param kwargs:
        :return:
        """

        import uvicorn

        uvicorn.config.LOGGING_CONFIG['formatters']['access']['fmt'] = f"""
        🔥 %(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s
        """.strip()
        uvicorn.run(
            app if app else self,  #
            host=host, port=port, workers=workers, access_log=access_log, reload=reload, **kwargs
        )

    @cached_property
    def limiter(self):
        """
            from meutils.serving.fastapi import App
            from fastapi import Request

            app = App()

            @app.get("/home")
            @app.limiter.limit("5/minute")
            async def homepage(request: Request): # 必须叫 request 。。。
                return "TEST"
        :return:
        """
        from slowapi.errors import RateLimitExceeded
        from slowapi import Limiter, _rate_limit_exceeded_handler
        from slowapi.util import get_remote_address

        limiter = Limiter(key_func=get_remote_address)

        self.state.limiter = limiter
        self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

        return limiter


if __name__ == '__main__':
    from fastapi import FastAPI, APIRouter, Request
    from meutils.serving.fastapi.utils import limit

    app = App()
    router = APIRouter()  # 怎么限流？


    @router.get('/xx', name='xxxx')
    @limit(limit_value='3/minute', error_message='请联系我')
    def f(request: Request):
        return {'1': '11'}


    app.include_router(router)
    app.run(port=8899)
