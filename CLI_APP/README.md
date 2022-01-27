# CLI APP USAGE

- Install the requirements.txt using (only pycurl was used).

```bash
pip install -r requirements.txt
```

- The app can be used as a menu based application or even as a one-liner cli command, Examples will be shown.

## CLI USAGE

- As a cli one-liner

```bash
python3 cliapp.py {username} {pass} -l # To see what files you have
python3 cliapp.py {username} {pass} -d {file1} {file2} ... # To Download
python3 cliapp.py {username} {pass} -u {file1} {file2} ... # To Upload
python3 cliapp.py {username} {pass} -upd {filenm_from} {filenm_to} # To Rename
python3 cliapp.py {username} {pass} -del {file1} {file2} ... # To Delete
python3 cliapp.py {username} {pass} -s {file1} {file2} ... # To Share (Shows list of avalilable users you can choose one or more)
```

> If it asks for authentication use either of these usr:pass pairs {"stan": "sword", "joe": "win", "may": "spi"}

## USAGE

- As a menu based:
  
```bash
# Login Prompt
YOUR DRIVE
ENTER YOUR USERNAME : joe
ENTER YOUR PASSWORD : win

# Options prompt
WELCOME joe
1. UPLOAD FILE 
2. DOWNLOAD FILE 
3. UPDATE FILE 
4. DELETE FILE 
5. SHARE 
6.LOGOUT
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  1.py


ENTER YOUR CHOICE (1-6) :
```

### TO Download

```bash
ENTER YOUR CHOICE (1-6) : 2
ENTER FILE NAMES TO DOWNLOAD WITH SPACE to SEPERATE : test.java 1.py
ENTER TO LOCATION either './' RELATIVE or ACTUAL '/home/...' OR just press enter : /home/jmarc/Desktop/
```

### TO Upload

```bash
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  1.py

ENTER YOUR CHOICE (1-6) : 1
ENTER FILE NAMES TO UPLOAD WITH SPACE to SEPERATE : /home/jmarc/Desktop/hello.png ./README.md
{"Uploaded_Filenames":["hello.png","README.md"]}
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  1.py
File 4  :  hello.png
```

### TO Update

```bash
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  1.py
File 4  :  hello.png

ENTER YOUR CHOICE (1-6) : 3   
ENTER FROM FILE NAME AND TO FILE NAME WITH SPACE to SEPERATE : 1.py wow.py
{"Updated_Filenames":{"From":"1.py","To":"wow.py"}}

YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  wow.py
File 4  :  hello.png

```

### TO Delete

```bash
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  wow.py
File 4  :  hello.png

ENTER YOUR CHOICE (1-6) : 4
ENTER FILE NAME/s TO DELETE WITH SPACE to SEPERATE : wow.py win.py
DELETED_FILE  :  wow.py
NOT_DELETED_FILE  :  TRY AGAIN

YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  hello.png
```

### TO Share

```bash
YOUR FILES:

File 0  :  wp2740153-berserk-guts-wallpaper.jpg
File 1  :  test.java
File 2  :  README.md
File 3  :  hello.png


ENTER YOUR CHOICE (1-6) : 5
CURRENT USERS  : 
stan
joe
may


ENTER FILE NAME/s TO SEND WITH SPACE to SEPERATE : test.java hello.png
ENTER TO USER NAME/s to send to WITH SPACE TO SEPERATE : stan may
FILE SHARED  :  test.java
TRANSFER  :  {'From': 'joe', 'To': 'stan'}
FILE SHARED  :  hello.png
TRANSFER  :  {'From': 'joe', 'To': 'stan'}


FILE SHARED  :  test.java
TRANSFER  :  {'From': 'joe', 'To': 'may'}
FILE SHARED  :  hello.png
TRANSFER  :  {'From': 'joe', 'To': 'may'}
```
