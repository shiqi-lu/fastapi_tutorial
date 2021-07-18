import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from coronavirus import application
from tutorial import app03, app04, app05, app07

# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(
    title="FastAPI Tutorial and Coronavirus Tracker API Docs",
    description='FastAPI教程 新冠病毒疫情跟踪器API接口文档，'
                '项目代码：https://github.com/shiqi-lu/fastapi_tutorial',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redocs',
)

# mount表示将某个目录下一个完全独立的应用挂载过来，这个不会在API交互文档中显示
# .mount()不要在分路由APIRouter().mount()调用，模板会报错
app.mount(path='/static', app=StaticFiles(directory='./coronavirus/static'), name='static')


# # 重写HTTPException异常处理器
# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     """
#     :param request: 这个参数不能省
#     :param exc:
#     :return:
#     """
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)


app.include_router(app03, prefix='/ch03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/ch04', tags=['第四章 响应处理和FastAPI配置'])
app.include_router(app05, prefix='/ch05', tags=['第五章 FastAPI的依赖注入系统'])

app.include_router(app07, prefix='/ch07', tags=['第七章 FastAPI的数据库操作和多应用的目录结构设计'])
app.include_router(application, prefix='/coronavirus', tags=['新冠病毒疫情跟踪器API'])

# uvicorn hello_world:app --reload

if __name__ == "__main__":
    uvicorn.run('run:app', host='0.0.0.0',
                port=8000, reload=True,
                debug=True, workers=1)
