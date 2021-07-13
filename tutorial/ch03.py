from enum import Enum
from fastapi import APIRouter, Path

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