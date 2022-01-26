from typing import Optional
from urllib.parse import urlencode
from io import BytesIO
import ast
import sys
import pycurl

# UPLOAD

BASE_URL = 'https://drive-cldwry-2k22.herokuapp.com/api/'


def uplo_file(usr, files):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, BASE_URL + usr + '/uploadfiles/')
    to_upload = [('file', (crl.FORM_FILE, file,)) for file in files]
    crl.setopt(crl.HTTPPOST, to_upload)
    crl.perform()
    crl.close()

# DOWN


def down_file(usr, files, to: str = ""):
    for file in files:
        with open(to+file, 'wb') as f:
            c = pycurl.Curl()
            c.setopt(c.URL, BASE_URL + usr + '/downfiles/' + file)
            c.setopt(c.WRITEDATA, f)
            c.perform()
            c.close()


def look_file(usr):
    b_obj = BytesIO()
    crl = pycurl.Curl()

    crl.setopt(crl.URL, BASE_URL + usr + '/look/')
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue()
    fin = ast.literal_eval(get_body.decode('utf8'))
    print('YOUR FILES:\n')
    for k, v in fin.items():
        print(k, " : ", v)

    print("\n")


def del_file(usr, files):
    for file in files:
        b_obj = BytesIO()
        crl = pycurl.Curl()

        crl.setopt(crl.URL, BASE_URL + usr + '/delefiles/'+file)
        crl.setopt(crl.WRITEDATA, b_obj)
        crl.perform()
        crl.close()
        get_body = b_obj.getvalue()
        fin = ast.literal_eval(get_body.decode('utf8'))
        # print('YOUR FILES:\n')
        for k, v in fin.items():
            print(k, " : ", v)

    print("\n")


def upd_file(usr, files):
    crl = pycurl.Curl()

    crl.setopt(crl.URL, BASE_URL + usr + '/updfiles/' + files[0])
    data = {'to': files[1]}
    print(data)
    pf = urlencode(data)
    crl.setopt(crl.FOLLOWLOCATION, True)

    crl.setopt(crl.POSTFIELDS, pf)
    crl.perform()
    crl.close()


def shr_file(to, usr, files):
    for u in to:
        for file in files:
            b_obj = BytesIO()
            crl = pycurl.Curl()

            crl.setopt(crl.URL, BASE_URL + usr + '/shrto/'+u+"/"+file)
            crl.setopt(crl.WRITEDATA, b_obj)
            crl.perform()
            crl.close()
            get_body = b_obj.getvalue()
            fin = ast.literal_eval(get_body.decode('utf8'))
            # print('YOUR FILES:\n')
            for k, v in fin.items():
                print(k, " : ", v)

    print("\n")


def curr_usr(usr):
    b_obj = BytesIO()
    crl = pycurl.Curl()

    crl.setopt(crl.URL, BASE_URL + 'cur_usr')
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue()
    fin = ast.literal_eval(get_body.decode('utf8'))
    for k, v in fin.items():
        print(k, " : ")
        for it in v:
            print(it)

    print("\n")
    return [i for i in fin["CURRENT USERS"] if i != usr]


def login(usrnm, passw):
    print(usrnm, passw)
    fl = False
    while(True):
        if fl:
            break
        print("WELCOME " + usrnm)
        print("1. UPLOAD FILE \n2. DOWNLOAD FILE \n3. UPDATE FILE \n4. DELETE FILE \n5. SHARE \n6.LOGOUT")
        look_file(usrnm)
        ch = input("ENTER YOUR CHOICE (1-6) : ")
        if ch == '1':
            fil = input("ENTER FILE NAMES TO UPLOAD WITH SPACE to SEPERATE : ")
            fil = fil.split(" ")
            uplo_file(usrnm, fil)
        elif ch == '2':
            fil = input("ENTER FILE NAMES TO DOWNLOAD WITH SPACE to SEPERATE : ")
            fil = fil.split(" ")
            to_loc = input("ENTER TO LOCATION either './' RELATIVE or ACTUAL '/home/...' OR just press enter : ")
            down_file(usrnm, fil, to_loc)
        elif ch == '3':
            fil = input("ENTER FROM FILE NAME AND TO FILE NAME WITH SPACE to SEPERATE : ")
            fil = fil.split(" ")
            upd_file(usrnm, fil)
        elif ch == '4':
            fil = input("ENTER FILE NAME/s TO DELETE WITH SPACE to SEPERATE : ")
            fil = fil.split(" ")
            del_file(usrnm, fil)
        elif ch == '5':
            chk = curr_usr(usrnm)
            fil = input("ENTER FILE NAME/s TO SEND WITH SPACE to SEPERATE : ")
            fil = fil.split(" ")
            to_usr = input("ENTER TO USER NAME/s to send to WITH SPACE TO SEPERATE : ")
            for to_u in to_usr.split(" "):
                if to_u in chk:
                    shr_file([to_u], usrnm, fil)
                else:
                    print("ENTER THE RIGHT TO USERNAME : ", to_u)
        elif ch == '6':
            fl = True
            break
        else:
            print("ENTER AN APPROPRIATE OPTION !!")
            continue
    return fl


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        fl = False
        while True:
            if fl:
                break
            print("YOUR DRIVE")
            usrnm = input("ENTER YOUR USERNAME : ")
            passw = input("ENTER YOUR PASSWORD : ")
            fl = login(usrnm, passw)
    else:
        if len(sys.argv) > 2:
            usrnm = sys.argv[1]
            passw = sys.argv[2]
            opre = sys.argv[3].split("-")
            files = sys.argv[4:]
            # print(usrnm, passw, opre, files)
            if "l" in opre:
                look_file(usrnm)
            elif 'u' in opre:
                uplo_file(usrnm, files)
            elif 'd' in opre:
                down_file(usrnm, files)
            elif 'upd' in opre:
                upd_file(usrnm, files)
            elif 'del' in opre:
                del_file(usrnm, files)
            elif 's' in opre:
                chk = curr_usr(usrnm)
                to_usr = input("ENTER TO USER NAME/s with SPACE TO SEPERATE : ")
                for to_u in to_usr.split(" "):
                    if to_u in chk:
                        shr_file([to_u], usrnm, files)
                    else:
                        print("ENTER THE RIGHT TO USERNAME")
            else:
                print("CHOOSE CORRECT OPERATION")

        else:
            print("INPUT YOUR USERNAME AND PASS PROPERLY!!!")
