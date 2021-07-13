from enum import Enum
from typing import Optional, List
from fastapi import APIRouter, Path, Query

app03 = APIRouter()

"""Path Parameters and Number Validations 路径参数和数字验证"""


@app03.get("/path/parameters")
def path_params01():
    return {"message": "This is a message"}


# 函数的顺序就是路由的顺序
@app03.get("/path/{parameters}")
def get_params02(parameters: str):
    return {"message": parameters}


# 枚举类
class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型的参数
def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "comfirmed": 1492, "death": 7}
    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 971, "death": 9}
    return {"city_name": city, "latest": "unknown"}


# 通过 path parameters 传递文件路径
@app03.get("/files/{file_path:path}")
def filepath(file_path: str):
    return f"The file path is {file_path}"


# 校验路径参数
@app03.get("/path_/{num}")
def path_params_validate(
        num: int = Path(..., title="Your Number",
                        description="懒得描述", ge=1, le=10)
):
    return num


"""Query Parameters and String Validations 查询参数和字符串验证"""


# 给了默认值就是选填的参数，没给默认值就是必填参数
@app03.get("/query")
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


# bool类型转换：yes on 1 True true会转换成true, 其它为false
@app03.get("/query/bool/conversion")
def type_comversion(param: bool = False):
    return param


# 长度+正则表达式验证，比如长度8-16位，以a开头。其它校验方法看Query类的源码
@app03.get("/query/validations")
def query_params_validate(
        value: str = Query(..., min_length=8, max_length=16,
                           regex="^a"),
        values: List[str] = Query(["v1, v2"], alias="the Sp name")
):
    return value, values
