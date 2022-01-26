import pycurl
import os
from io import BytesIO
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
    # Set URL value
    crl.setopt(crl.URL, BASE_URL + usr + '/look/')
    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)

    # Perform a file transfer
    crl.perform()

    # End curl session
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters)
    get_body = b_obj.getvalue()

    # Decode the bytes stored in get_body to HTML and print the result
    print('Output of GET request:\n%s' % get_body.decode('utf8'))


def dele_file(usr, files):
    pass


def upd_file(usr, files):
    pass


def shr_file(to, usr, files):
    pass


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
            pass
        elif ch == '6':
            fl = True
            break
        else:
            print("ENTER AN APPROPRIATE OPTION !!")
            continue
    return fl


if __name__ == '__main__':
    fl = False
    while True:
        if fl:
            break
        print("YOUR DRIVE")
        usrnm = input("ENTER YOUR USERNAME : ")
        passw = input("ENTER YOUR PASSWORD : ")
        fl = login(usrnm, passw)
