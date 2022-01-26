from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, FastAPI, HTTPException, status
import secrets
import os
import shutil
from starlette.responses import FileResponse, RedirectResponse
from fastapi import FastAPI, Form, Response, UploadFile, File, APIRouter, Query, HTTPException, Request, status, Depends
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


upload_folder = "./fil/"
TEMPLATES = Jinja2Templates(directory="templates/")


app = FastAPI()

fake_db = {"stan": "sword", "joe": "win", "may": "spi"}


security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    for k, v in fake_db.items():
        correct_username = secrets.compare_digest(credentials.username, k)
        correct_password = secrets.compare_digest(credentials.password, v)
        if not (correct_username and correct_password):
            continue
        else:
            break
    if not (correct_username and correct_password):
        fake_db[credentials.username] = credentials.password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login again",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/")
def read_current_user(username: str = Depends(get_current_username),  request: Request = Optional):
    # return {"username": username}
    try:
        temp = os.listdir(upload_folder + username + "/")
    except:
        os.mkdir(upload_folder + username + "/")
        temp = os.listdir(upload_folder + username + "/")

    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse("index.html",
                                      {"request": request, "recipes": files, "usr": username,
                                       "av": [i for i in fake_db.keys() if i != username]},)


@app.post("/{usr}/uploadfiles/")
async def create_file(usr, request: Request = Optional, file: List[UploadFile] = File(...)):
    print(usr)
    global upload_folder
    for f in file:
        file_object = f.file
        # create empty file to copy the file_object to
        up_fol = open(os.path.join(upload_folder + usr + "/", f.filename), 'wb+')
        shutil.copyfileobj(file_object, up_fol)
        up_fol.close()

    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")

    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
    )
    # return {"filenames": [fil.filename for fil in file]}


@app.post("/api/{usr}/uploadfiles/")
async def create_file_api(usr, request: Request = Optional, file: List[UploadFile] = File(...)):
    print(usr)
    global upload_folder
    for f in file:
        file_object = f.file
        # create empty file to copy the file_object to
        up_fol = open(os.path.join(upload_folder + usr + "/", f.filename), 'wb+')
        shutil.copyfileobj(file_object, up_fol)
        up_fol.close()
    return {"Uploaded_Filenames": [fil.filename for fil in file]}


@app.get("/logout")
async def logout(credentials: HTTPBasicCredentials = Depends(security), request: Request = Optional):
    try:
        temp = os.listdir(upload_folder + credentials.username + "/")
    except:
        os.mkdir(upload_folder + credentials.username + "/")
        temp = os.listdir(upload_folder + credentials.username + "/")

    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse("index.html",
                                      {"request": request, "recipes": files, "usr": credentials.username,
                                       "av": [i for i in fake_db.keys() if i != credentials.username]},)


@app.get('/{usr}')
@app.get("/{usr}/look/")
async def lookup_file(usr: str, request: Request) -> dict:
    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")
    print(usr)
    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
    )


@app.get("/api/{usr}/look/")
async def lookup_file_api(usr: str, request: Request) -> dict:
    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")
    print(usr)
    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return files


@app.get("/{usr}/delefiles/{fname}")
async def del_file(usr, fname, request: Request = Optional):

    print(usr)
    try:
        os.remove(upload_folder + usr + "/" + fname)
        try:
            temp = os.listdir(upload_folder + usr + "/")
        except:
            os.mkdir(upload_folder + usr + "/")
            temp = os.listdir(upload_folder + usr + "/")
        files = {}
        for i, a in enumerate(temp):
            files["File "+str(i)] = a
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "recipes": files, "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
        )
    except:
        try:
            temp = os.listdir(upload_folder + usr + "/")
        except:
            os.mkdir(upload_folder + usr + "/")
            temp = os.listdir(upload_folder + usr + "/")
        files = {}
        for i, a in enumerate(temp):
            files["File "+str(i)] = a
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "recipes": files, "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
        )


@app.get("/api/{usr}/delefiles/{fname}")
async def del_file_api(usr, fname, request: Request = Optional):

    print(usr)
    try:
        os.remove(upload_folder + usr + "/" + fname)
        try:
            temp = os.listdir(upload_folder + usr + "/")
        except:
            os.mkdir(upload_folder + usr + "/")
            temp = os.listdir(upload_folder + usr + "/")

        return {"DELETED_FILE": fname}
    except:
        return {"DELETED_FILE": "TRY AGAIN"}


@app.post("/{usr}/updfiles/{fro}/")
async def updfiles(usr, fro: str, to: str = Form(...), request: Request = Optional):
    print(usr)
    if not "." in to:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to + "." + fro.split(".")[1])

    else:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to)

    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")
    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
    )


@app.post("/api/{usr}/updfiles/{fro}/")
async def updfiles_api(usr, fro: str, to: str = Form(...), request: Request = Optional):
    print(usr)
    if not "." in to:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to + "." + fro.split(".")[1])

    else:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to)

    return {"Updated_Filenames": {"From": fro, "To": to}}


@app.get('/{usr}/shrto/{ur}/{tem}')
async def shrto(usr, ur, tem, request: Request = Optional):
    try:
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)
        print(usr, ur, tem)
    except:
        os.mkdir(upload_folder + ur + "/")
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)
    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")
    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
    )


@app.get('/api/{usr}/shrto/{ur}/{tem}')
async def shrto_api(usr, ur, tem, request: Request = Optional):
    try:
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)
        print(usr, ur, tem)
    except:
        os.mkdir(upload_folder + ur + "/")
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)

    return {"FILE SHARED": tem, "TRANSFER": {"From": usr, "To": ur}}


@ app.get("/{usr}/downfiles/{fname}")
async def down_file(usr, fname):
    print(usr)
    return FileResponse(upload_folder + usr + "/"+fname, media_type='application/octet-stream', filename=fname)


@ app.get("/api/{usr}/downfiles/{fname}")
async def down_file_api(usr, fname):
    print(usr)
    return FileResponse(upload_folder + usr + "/"+fname, media_type='application/octet-stream', filename=fname)


@app.get("/api/cur_usr")
async def send_usrs():
    return {"CURRENT USERS": [i for i in fake_db.keys()]}
