import shutil
import typing as t
from datetime import datetime

import bcrypt
from fastapi import FastAPI, File, UploadFile, Form, Header, Depends
from fastapi.responses import JSONResponse
from piccolo_admin.endpoints import create_admin
from piccolo_api.crud.serializers import create_pydantic_model
from piccolo.engine import engine_finder
from pydantic import BaseModel
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from home.endpoints import HomeEndpoint
from home.piccolo_app import APP_CONFIG
from home.tables import Task, NewUser, DeviceUser, Device, Attendance, Firm
from utils import create_jwt_token, extract_token

app = FastAPI(
    routes=[
        Route("/", HomeEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
        Mount("/images/", StaticFiles(directory="images")),

    ],
)

TaskModelIn: t.Any = create_pydantic_model(table=Task, model_name="TaskModelIn")
TaskModelOut: t.Any = create_pydantic_model(
    table=Task, include_default_columns=True, model_name="TaskModelOut"
)


# NewUserModelIn: t.Any = create_pydantic_model(table=NewUser, model_name="NewUserModelIn")\
class NewUserModelIn(BaseModel):
    user_name: str
    password: str
    first_name: str
    last_name: str
    user_image: str


class NewUserModelOut(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    user_image: str


class CreateFirmModelOut(BaseModel):
    firm_name: str
    firm_image: str
    firm_address: str
    firm_latitude: str
    firm_longitude: str
    firm_contact_number: str
    firm_mail_address: str
    firm_type: str


class LoginUserModelIn(BaseModel):
    user_name: str
    password: str
    device_id: str
    device_name: str
    device_OS_name: str
    device_build_number: str
    device_finger_print: str


class ClockInModel(BaseModel):
    check_in_latitude: str
    check_in_longitude: str
    check_in_address: str


class CreateFirmModel(BaseModel):
    firm_name: str
    firm_image: str
    firm_address: str
    firm_latitude: str
    firm_longitude: str
    firm_contact_number: str
    firm_mail_address: str
    firm_type: str


class ClockOutModel(BaseModel):
    id: int
    check_out_latitude: str
    check_out_longitude: str
    check_out_address: str


@app.get("/tasks/", response_model=t.List[TaskModelOut])
async def tasks():
    return await Task.select().order_by(Task.id)


@app.get("/get_user/", response_model=NewUserModelOut)
async def get_user(ids: tuple[int, int] = Depends(extract_token)):
    user = await NewUser.objects().get(NewUser.id == ids[1])
    return NewUserModelOut(user_name=user.user_name, first_name=user.first_name,
                           last_name=user.last_name, user_image=user.user_image)


@app.get("/get_firm/", response_model=CreateFirmModelOut)
async def get_firm(ids: tuple[int, int] = Depends(extract_token)):
    firm_detail = await Firm.objects().get(Firm.user_id == ids[1])
    return CreateFirmModelOut(firm_name=firm_detail.firm_name,
                              firm_address=firm_detail.firm_address, firm_latitude=firm_detail.firm_latitude,
                              firm_longitude=firm_detail.firm_longitude, firm_contact_number=firm_detail.contact_number,
                              firm_mail_address=firm_detail.mail_address, firm_type=firm_detail.firm_type)


@app.post("/login/", response_model=dict)
async def login(login_model: LoginUserModelIn):
    login_user = await NewUser.objects().get(NewUser.user_name == str(login_model.user_name))
    if login_user:
        if bcrypt.checkpw(login_model.password.encode('utf-8'), bytes(login_user.password, 'utf-8')):
            device = Device(device_id=login_model.device_id, device_name=login_model.device_name,
                            device_OS_name=login_model.device_OS_name,
                            device_build_number=login_model.device_build_number,
                            device_finger_print=login_model.device_finger_print)
            await device.save()
            device_user = DeviceUser(device_id=device.id, user_id=login_user.id, )
            await device_user.save()
            token = create_jwt_token({
                "sub": login_user.id,
                "did": device.id,
                "type": "A",
            },
                is_refreshed_token=False,
            )
            refreshed_token = create_jwt_token({
                "sub": login_user.id,
                "did": device.id,
                "type": "R",
            },
                is_refreshed_token=True,
            )
            return {"message": "Login successfully", "Token id": token, "Refresh token": refreshed_token}
    return {"message": "Invalid Password or user name"}


#
# @app.post("/new_users/", response_model=dict)
# async def register_user(new_user_model: t.Annotated[NewUserModelIn, Form()], file: t.Annotated[UploadFile, File()]):
#     try:
#         if not new_user_model.user_name:
#             return {"message": "User name can not be empty"}
#         if not new_user_model.password:
#             return {"message": "Password can not be empty"}
#         new_user = await NewUser.objects().get(NewUser.user_name == str(new_user_model.user_name))
#         if new_user:
#             return {"message": "User already exist"}
#         new_user = NewUser(**new_user_model.dict())
#         new_user.user_image = file.filename
#         with open(f"images/{new_user_model.user_image}", "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
#         salt = bcrypt.gensalt()
#         hashed = bcrypt.hashpw(bytes(new_user_model.password, 'utf-8'), salt)
#         new_user.password = str(hashed, 'utf-8')
#         await new_user.save()
#         return {"message": "Register Successfully"}
#
#     except Exception as e:
#         return {"message": e}


@app.post("/clock_in/", response_model=dict)
async def clock_in(clock_in_model: ClockInModel, ids: tuple[int, int] = Depends(extract_token)):
    try:
        user_clock_in = Attendance(
            user_id=ids[1],
            check_in_latitude=clock_in_model.check_in_latitude,
            check_in_longitude=clock_in_model.check_in_longitude,
            check_in_address=clock_in_model.check_in_address,
            device_id=ids[0]
        )
        await user_clock_in.save()
        return {"message": "Clocked In Successfully", "id": user_clock_in.id}
    except Exception as e:
        print(e)
        return {"error": e}


# Todo :-  this is form data ...please convert it into multipart and form data
@app.post("/add_firm/", response_model=dict)
async def add_firm(firm_model: CreateFirmModel, ids: tuple[int, int] = Depends(extract_token)):
    try:
        create_firm = Firm(
            user_id=ids[1],
            firm_name=firm_model.firm_name,
            firm_image=firm_model.firm_image,
            contact_number=firm_model.firm_contact_number,
            mail_address=firm_model.firm_mail_address,
            firm_address=firm_model.firm_address,
            firm_latitude=firm_model.firm_latitude,
            firm_longitude=firm_model.firm_longitude,
            firm_type=firm_model.firm_type,
            device_id=ids[0]
        )
        await create_firm.save()
        return {"message": "Firm Created Successfully"}
    except Exception as e:
        print(e)
        return {"error": e}


@app.post("/clock_out/", response_model=dict)
async def clock_in(clock_out_model: ClockOutModel, ids: tuple[int, int] = Depends(extract_token)):
    try:
        attendance = await Attendance.objects().get(Attendance.id == clock_out_model.id)
        if attendance:
            attendance.check_out_address = clock_out_model.check_out_address
            attendance.check_out_latitude = clock_out_model.check_out_latitude
            attendance.check_out_longitude = clock_out_model.check_out_longitude
            attendance.clock_out_time = datetime.now()
            await attendance.save()
            return {"message": "Clocked Out Successfully"}
        return {"Error": "Invalid Attendance Id"}
    except Exception as e:
        print(e)
        return {"error": e}


@app.post("/new_users_image/", response_model=dict)
async def register_user(user_name: t.Annotated[str, Form()], password: t.Annotated[str, Form()],
                        first_name: t.Annotated[str, Form()], last_name: t.Annotated[str, Form()],
                        user_image: t.Annotated[UploadFile, File()]):
    if not user_name:
        return {"message": "User name can not be empty"}
    if not password:
        return {"message": "Password can not be empty"}
    new_user = await NewUser.objects().get(NewUser.user_name == str(user_name))
    if new_user:
        return {"message": "User already exist"}
    new_user = NewUser(user_name=user_name, user_image=f"images/{user_image.filename}", first_name=first_name,
                       last_name=last_name,
                       )
    with open(f"images/{user_image.filename}", "wb") as buffer:
        shutil.copyfileobj(user_image.file, buffer)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
    new_user.password = str(hashed, 'utf-8')
    await new_user.save()
    return {"message": "Register Successfully"}


@app.put("/tasks/{task_id}/", response_model=TaskModelOut)
async def update_task(task_id: int, task_model: TaskModelIn):
    task = await Task.objects().get(Task.id == task_id)
    if not task:
        return JSONResponse({}, status_code=404)

    for key, value in task_model.dict().items():
        setattr(task, key, value)

    await task.save()

    return task.to_dict()


@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    task = await Task.objects().get(Task.id == task_id)
    if not task:
        return JSONResponse({}, status_code=404)

    await task.remove()

    return JSONResponse({})


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
