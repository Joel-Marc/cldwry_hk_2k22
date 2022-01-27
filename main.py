from fastapi.templating import Jinja2Templates
from typing import Optional, List
from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request, Depends
from starlette.responses import FileResponse, RedirectResponse
import shutil
import os
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import pymongo
import hashlib
from PIL import Image
# from pydub import AudioSegment


client = pymongo.MongoClient(
    "mongodb+srv://joe:marc@cluster0.ooljk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

coll = db['users']


fake_db = {}
for i in coll.find({}):
    # temp = {}
    fake_db[i['username']] = i['phash']

app = FastAPI()


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
    """
    Renders the main page for the WEB-APP
    """
    return TEMPLATES.TemplateResponse(
        "login.html",
        {"request": request},
    )


@app.post('/login')
def login(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    """
    Logs in for the WEB-APP, checks if pass hash matches and creates a cookie for the session and redirects to /look of the user
    """

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


@app.post('/regist')
def regist(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    """
    Registers for WEB-APP by adding the document to MongoDB Cluster, makes a cookie for the session and redirects to /look of the user
    """
    coll = db['users']
    phash = hashlib.sha256(password.encode()).hexdigest()

    # print(hashlib.sha256('win'.encode()).hexdigest())
    # coll.insert_many(
    #     [{'username': 'joe', 'phash': hashlib.sha256("win".encode()).hexdigest()},
    #      {'username': 'may', 'phash': hashlib.sha256("spi".encode()).hexdigest()},
    #      {'username': 'stan', 'phash': hashlib.sha256("sword".encode()).hexdigest()}])
    # # coll.delete_many({})

    fin = {'username': username, 'phash': phash}

    coll.insert_one(fin)

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=username)
    refresh_token = Authorize.create_refresh_token(subject=username)

    coll = db['users']

    for i in coll.find({}):
        # temp = {}
        fake_db[i['username']] = i['phash']

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    response = RedirectResponse(url="/"+username+"/look/")
    return response


@app.post('/api/login')
def login_api(username: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):
    """
    Logs in for thr CLI-APP, checks if pass hash matches and creates a cookie for the session and redirects to /look of the user
    """
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
        # response = RedirectResponse(url="/")
        return "nope"
        # raise HTTPException(status_code=401, detail="Bad username or password")

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
    """ 
    LOGS OUT for the WEB-APP , UNSETS THE JWT Token in Cookies , redirects to root page /
    """
    # Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    response = RedirectResponse(url="/")
    return response

    return {"msg": "Successfully logout"}

    # print(fin)


@app.post("/{usr}/uploadfiles/")
async def create_file(usr, request: Request = Optional, file: List[UploadFile] = File(...), Authorize: AuthJWT = Depends()):
    """ 
    The way WEB-APP Uploads and then renders the main page 
    """
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
        # elif spfnm[-1] in ['mp3', 'flac']:
        #     raw_audio = AudioSegment.from_file(upload_folder + usr + "/" + f.filename,
        #                                        frame_rate=44100, channels=2, sample_width=2)
        #     raw_audio.export(upload_folder + usr + "/" + ".".join(spfnm[:-1]) + '.mp3', format="mp3")
        #     os.remove(upload_folder + usr + "/" + f.filename)

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
    """ 
    The way CLI-APP Uploads and then returns appropriate response either the uploaded filename or not 
    """
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
    """ 
    The way WEB-APP renders the main page with all the file names and operations
    """
    print(Authorize.get_jwt_subject())
    try:
        temp = os.listdir(upload_folder + usr + "/")
    except:
        os.mkdir(upload_folder + usr + "/")
        temp = os.listdir(upload_folder + usr + "/")
    print(usr, fake_db.keys())
    files = {}
    for i, a in enumerate(temp):
        files["File "+str(i)] = a
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": files,  "usr": usr, "av": [i for i in fake_db.keys() if i != usr]},
    )


@app.get("/api/{usr}/look/")
async def lookup_file_api(usr: str, request: Request, Authorize: AuthJWT = Depends()) -> dict:
    """ 
    The way CLI-APP gets the file name list of the user
    """
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
    """ 
    The way WEB-APP Deletes the file
    """
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
    """ 
    The way CLI-APP Deletes and then returns appropriate response either the deleted filename or not 
    """
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
    """ 
    The way WEB-APP Updates the file and then renders the main page 
    """
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
    """ 
    The way CLI-APP Updates and then returns appropriate response either the updated filename or not 
    """
    print(usr)
    if not "." in to:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to + "." + fro.split(".")[-1])

    else:
        os.rename(upload_folder + usr + "/" + fro, upload_folder + usr + "/" + to)

    return {"Updated_Filenames": {"From": fro, "To": to}}


@app.get('/{usr}/shrto/{ur}/{tem}')
async def shrto(usr, ur, tem, request: Request = Optional, Authorize: AuthJWT = Depends()):
    """ 
    The way WEB-APP Shares the file and then renders the main page 
    """
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
    """ 
    The way CLI-APP shares and then returns appropriate response either the shared filename  and how transfer happned or not 
    """
    try:
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)
        print(usr, ur, tem)
    except:
        os.mkdir(upload_folder + ur + "/")
        shutil.copyfile(upload_folder + usr + "/" + tem, upload_folder + ur + "/" + tem)
        tem = "NOT SHARED"

    return {"FILE SHARED": tem, "TRANSFER": {"From": usr, "To": ur}}


@ app.get("/{usr}/downfiles/{fname}")
async def down_file(usr, fname,  request: Request = Optional, Authorize: AuthJWT = Depends()):
    """ 
    The way WEB-APP Downloads and then renders the main page 
    """
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
    """ 
    The way CLI-APP Downloads and then returns appropriate response 
    """
    print(usr)
    return FileResponse(upload_folder + usr + "/"+fname, media_type='application/octet-stream', filename=fname)


@app.get("/{usr}/prevget/{fname}")
async def prev_file(usr, fname):
    """ 
    The way WEB-APP gets the preview and then renders it in the main page 
    """
    print(fname.split('.')[-1])
    # return {"The directory": os.path.realpath(upload_folder + usr + "/"+fname)}
    return FileResponse(upload_folder + usr + "/"+fname)


@app.get("/api/cur_usr")
async def send_usrs():
    """ 
    The way CLI-APP gets the current users from the db 
    """
    return {"CURRENT USERS": [i for i in fake_db.keys()]}
