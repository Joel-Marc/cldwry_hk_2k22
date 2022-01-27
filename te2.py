from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request, Depends
from starlette.responses import FileResponse, RedirectResponse
import shutil
import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import pymongo
import hashlib
from PIL import Image
from pydub import AudioSegment
import sys
import ffprobe

sys.path.append('./ffmpeg')


client = pymongo.MongoClient(
    "mongodb+srv://joe:marc@cluster0.ooljk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

app = FastAPI()

fake_db = {"stan": "sword", "joe": "win", "may": "spi"}


upload_folder = "./fil/"
TEMPLATES = Jinja2Templates(directory="templates/")


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get('/')
@app.post('/')
def firs(request: Request):
    return TEMPLATES.TemplateResponse(
        "login.html",
        {"request": request},
    )


@app.post('/login')
def login(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    coll = db['users']

    # print(hashlib.sha256('win'.encode()).hexdigest())
    # coll.insert_many(
    #     [{'username': 'joe', 'phash': hashlib.sha256("win".encode()).hexdigest()},
    #      {'username': 'may', 'phash': hashlib.sha256("spi".encode()).hexdigest()},
    #      {'username': 'stan', 'phash': hashlib.sha256("sword".encode()).hexdigest()}])
    # # coll.delete_many({})
    fin = {}
    for i in coll.find({'username': username}):
        # temp = {}
        fin[i['username']] = i['phash']
        print(fin)

    ckhash = hashlib.sha256(password.encode()).hexdigest()
    if username not in fin.keys() or ckhash not in fin.values():
        response = RedirectResponse(url="/")
        return response
        raise HTTPException(status_code=401, detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=username)
    refresh_token = Authorize.create_refresh_token(subject=username)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    response = RedirectResponse(url="/"+username+"/look/")
    return response


@app.post('/api/login')
def login_api(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    if username not in fake_db.keys() or password not in fake_db.values():
        return "nope"
        raise HTTPException(status_code=401, detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=username)
    refresh_token = Authorize.create_refresh_token(subject=username)

    return access_token


@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@app.get('/logout')
def logout(Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    response = RedirectResponse(url="/")
    return response

    return {"msg": "Successfully logout"}


@app.post("/{usr}/uploadfiles/")
async def create_file(usr, request: Request = Optional, file: List[UploadFile] = File(...), Authorize: AuthJWT = Depends()):
    print(usr)
    global upload_folder
    for f in file:
        file_object = f.file
        # create empty file to copy the file_object to
        up_fol = open(os.path.join(upload_folder + usr + "/", f.filename), 'wb+')
        shutil.copyfileobj(file_object, up_fol)
        up_fol.close()
        spfnm = f.filename.split('.')
        if spfnm[-1] in ['jpg', 'png', 'jpeg', 'gif', 'raw']:
            im = Image.open(upload_folder + usr + "/" + f.filename)
            rgb_im = im.convert('RGB')
            rgb_im.save(upload_folder + usr + "/" + ".".join(spfnm[:-1]) + '.jpg')
            os.remove(upload_folder + usr + "/" + f.filename)
        elif spfnm[-1] in ['mp3', 'flac']:
            raw_audio = AudioSegment.from_file(upload_folder + usr + "/" + f.filename,
                                               frame_rate=44100, channels=2, sample_width=2)
            raw_audio.export(upload_folder + usr + "/" + ".".join(spfnm[:-1]) + '.mp3', format="mp3")
            os.remove(upload_folder + usr + "/" + f.filename)

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


# @app.get('/{usr}')
@app.get("/{usr}/look/")
@app.post("/{usr}/look/")
async def lookup_file(usr: str, request: Request, Authorize: AuthJWT = Depends()) -> dict:
    print(Authorize.get_jwt_subject())
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
async def lookup_file_api(usr: str, request: Request, Authorize: AuthJWT = Depends()) -> dict:
    print(Authorize.get_jwt_subject())
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
async def del_file(usr, fname, request: Request = Optional, Authorize: AuthJWT = Depends()):

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
        return {"NOT_DELETED_FILE": "TRY AGAIN"}


@app.post("/{usr}/updfiles/{fro}/")
async def updfiles(usr, fro: str, to: str = Form(...), request: Request = Optional, Authorize: AuthJWT = Depends()):
    print(usr)
    if not "." in to:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to + "." + fro.split(".")[-1])

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
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to + "." + fro.split(".")[-1])

    else:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to)

    return {"Updated_Filenames": {"From": fro, "To": to}}


@app.get('/{usr}/shrto/{ur}/{tem}')
async def shrto(usr, ur, tem, request: Request = Optional, Authorize: AuthJWT = Depends()):
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
async def down_file(usr, fname,  request: Request = Optional, Authorize: AuthJWT = Depends()):
    try:
        temp = os.path.abspath(upload_folder + usr + "/" + fname)
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
            {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
        )
    print(usr, temp)
    return FileResponse(upload_folder + usr + "/"+fname, media_type='application/octet-stream', filename=fname)


@ app.get("/api/{usr}/downfiles/{fname}")
async def down_file_api(usr, fname):
    print(usr)
    return FileResponse(upload_folder + usr + "/"+fname, media_type='application/octet-stream', filename=fname)


@app.get("/{usr}/prevget/{fname}")
async def prev_file(usr, fname):
    print(fname.split('.')[-1])
    # return {"The directory": os.path.realpath(upload_folder + usr + "/"+fname)}
    return FileResponse(upload_folder + usr + "/"+fname)


@app.get("/api/cur_usr")
async def send_usrs():
    return {"CURRENT USERS": [i for i in fake_db.keys()]}
