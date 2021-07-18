from typing import Optional, List

from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr

app04 = APIRouter()

"""Response Model 响应模型"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str] = None


users = {
    "user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "123456", "email": "user02@example.com", "mobile": "110"}
}


# response_model 都是路径操作
# response_model_exclude_unset 表示不包含 Userout 的默认值，只包含实际值，如果没有则不包含
@app04.post("/response_model", response_model=UserOut, response_model_exclude_unset=True)
def response_model(user: UserIn):
    print(user.password)
    return users["user01"]


@app04.post(
    "/response_model/attributes",
    response_model=UserOut,
    # response_model=Union[UserIn, UserOut],
    # response_model=List[UserOut],
    response_model_include=["username", "email", "mobile"],
    response_model_exclude=["mobile"]
)
async def response_model_attributes(user: UserIn):
    """response_model_include列出需要在返回结果中包含的字段；response_model_exclude列出需要在返回结果中排除的字段"""
    # del user.password  # Union[UserIn, UserOut]后，删除password属性也能返回成功
    return user
    # return [user, user]


"""Response Status Code 响应状态码"""


@app04.post("/status_code", status_code=200)
def status_code():
    return {"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
def status_attribte():
    return {"status_code": status.HTTP_200_OK}


"""Form Data 表单数据处理"""


@app04.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    """用Form类需要pip install python-multipart; Form类的元数据和校验方法类似Body/Query/Path/Cookie"""
    return {"username": username}


"""Request Files 单文件、多文件上传及参数详解"""


@app04.post("/file")
async def file_(file: bytes = File(...)):
    # 如果要上传多个文件 files: List[bytes] = File(...)
    """使用File类 文件内容会以bytes的形式读入内存 适合于上传小文件"""
    return {"file_size": len(file)}


@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
        使用UploadFile类的优势:
        1.文件存储在内存中，使用的内存达到阈值后，将被保存在磁盘中
        2.适合于图片、视频大文件
        3.可以获取上传的文件的元数据，如文件名，创建时间等
        4.有文件对象的异步接口
        5.上传的文件是Python文件对象，可以使用write(), read(), seek(), close()操作
    """
    for file in files:
        contents = await file.read()
        print(contents)
    return {"filename": files[0].filename, "content_type": files[0].content_type}


"""【见run.py】FastAPI项目的静态文件配置"""

"""Path Operation Configuration 路径操作配置"""


@app04.post(
    "/path_operation_configuration",
    response_model=UserOut,
    # tags=["path"],
    description="This is summary",
    response_description="This is response description",
    deprecated=True,
    status_code=status.HTTP_202_ACCEPTED
)
async def path_operation(user: UserIn):
    """
        Path Operation Configuration 路径操作配置
        :param user: 用户信息
        :return: 返回结果
        """
    return user.dict()


"""Handling Errors 错误处理"""


@app04.get("/http_exception")
async def http_exception(city: str):
    if city != "Beijing":
        raise HTTPException(status_code=404, detail="City not found!",
                            headers={"X-Error": "Error"})
    return {"city": city}


@app04.get("/http_exception/{city_id}")
async def override_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(status_code=418, detail="NONOONONON!!")
    return {"city_id": city_id}
