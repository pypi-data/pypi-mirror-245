import sys
import time
import traceback
from fastapi import FastAPI, Response, Request
from chariot_scaffold import version, log
from chariot_scaffold.api_server.router import ActionRouter


app = FastAPI(title="千乘SOAR", version=version, description="YYDS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
app.include_router(ActionRouter(), tags=["动作"])


async def sieve_middleware(request: Request, call_next):
    s_time = time.perf_counter()    # todo 计时待优化

    try:    # 为了防止fastapi因为奇怪的逻辑挂掉
        response = await call_next(request)
        e_time = time.perf_counter()
        c_time = e_time - s_time
        cost = "%.5fs" % c_time if c_time < 0 else "%.5fms" % (c_time * 1000)
        log.debug(f"{request.client.host}:{request.client.port} | {response.status_code} | {cost} | {request.method} | {request.url}")
        return response
    except Exception:   # noqa
        e_time = time.perf_counter()
        c_time = e_time - s_time
        cost = "%.5fs" % c_time if c_time < 0 else "%.5fms" % (c_time * 1000)
        log.info(f"{request.client.host}:{request.client.port} | {500} | {cost} | {request.method} | {request.url}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback)
        log.error("\n" + exc_type.__name__ + " " + str(exc_value))
        return Response(f"{exc_type.__name__} {exc_value}", status_code=500)



app.middleware('http')(sieve_middleware)


def runserver(workers):
    import uvicorn
    uvicorn.run(
        "chariot_scaffold.api_server.app:app", host="0.0.0.0", port=10001, workers=workers, reload=True,
        log_level="critical"
    )
