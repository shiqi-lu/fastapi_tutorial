from typing import Optional
from fastapi import APIRouter, Depends

app05 = APIRouter()

"""Dependencies 创建、导入和声明依赖"""


async def common_parameters(q: Optional[str] = None,
                            page: int = 1,
                            limit: int = 100):
    return {"q": q, "page": page, "limit": limit}


@app05.get("/dependency01")
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


@app05.get("/dependency02")
def dependency02(commons: dict = Depends(common_parameters)):
    # 可以在async def中调用def依赖，也可以在def中导入async def依赖
    return commons
