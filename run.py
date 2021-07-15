import uvicorn
from fastapi import FastAPI

from coronavirus import application
from tutorial import app03, app04, app05, app07

app = FastAPI()

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
