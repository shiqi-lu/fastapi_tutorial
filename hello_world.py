from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CityInfo(BaseModel):
    province: str
    country: str
    # 与bool的区别是可以不传，默认是null
    is_affected: Optional[bool] = None


@app.get('/')
def hello_world():
    return {'hello': 'world'}


# 路径参数需要定义在路径+参数中，查询参数只需要定义在参数中
@app.get('/city/{city}')
def result(city: str, query_string: Optional[str] = None):
    return {'city': city, 'query_string': query_string}


@app.put('/city/{city}')
def result(city: str, city_info: CityInfo):
    return {'city': city, 'country': city_info.country,
            'is_affected': city_info.is_affected}

# 启动命令：uvicorn hello_world:app --reload
