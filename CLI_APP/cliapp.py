import pycurl
import os
from io import BytesIO
import ast
import sys
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


def down_file(usr, files):
    for file in files:
        with open(file, 'wb') as f:
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
    pass


def upd_file(usr, files):
    pass


def shr_file(to, usr, files):
    pass


def curr_usr():
    b_obj = BytesIO()
    crl = pycurl.Curl()

    crl.setopt(crl.URL, BASE_URL + 'cur_usr')
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.perform()
    crl.close()
    get_body = b_obj.getvalue()
    print(get_body.decode('utf8'))
    fin = ast.literal_eval(get_body.decode('utf8'))
    for k, v in fin.items():
        print(k, " : ", v)

    print("\n")


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
            pass
        elif ch == '2':
            pass
        elif ch == '3':
            pass
        elif ch == '4':
            pass
        elif ch == '5':
            curr_usr()
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
            print(usrnm, passw, opre, files)
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
                curr_usr()
            else:
                print("CHOOSE CORRECT OPERATION")

        else:
            print("INPUT YOUR USERNAME AND PASS PROPERLY!!!")
