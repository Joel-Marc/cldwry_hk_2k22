# cldwry_hk_2k22

- The WEB-APP is [ACTIVE HERE](https://drive-cldwry-2k22.herokuapp.com/) DEMO VIDEO [Here](https://drive.google.com/file/d/1OOKMo7FlSpO9lMwOf2oxPPJsvIxuUDky/view?usp=sharing)
- The CLI-APP doc is [HERE](https://github.com/Joel-Marc/cldwry_hk_2k22/blob/master/CLI_APP/README.md) DEMO VIDEO [Here](https://drive.google.com/file/d/1KHnlLSwQca4Bd9-L1y69MIh5MGG8yfnY/view?usp=sharing)

- Libraries Used - FastAPI, pymongo, PIL, hashlib FOR the Backend, jinja2 -> Web-APP, pycurl -> CLI-APP

## Features of WEB-APP

- Login over HTTP , hash of password is checked by retriving from MongoDB Cluster in MongoDB Atlas.
- UPLOAD one or More File/s At a time - Image Compression using Pillow Library - (i wasnt able to do audio or video compression because heroku doesnt allow ffmpeg library installation)
- Download Files (shows preview of the file too)
- Re-Name Files (can be exact name with file extention or with out one)
- Delete Files
- Share Files
- LogOut

All operations are straight Forward

> If it asks for authentication use either of these usr:pass pairs {"stan": "sword", "joe": "win", "may": "spi", "mith": "run", "cloud": "wiry"}

The blob storage application should have the following features:

1. ~~Checkpoint A - User authentication and session management~~ (Technically done)
2. ~~Checkpoint B - Implementation of the blob storage server~~
3. ~~Checkpoint C - Client application (CLI/ web based) for file upload, download, rename and delete~~ (BOTH DONE)
4. ~~Checkpoint D - User based access control on who can access the files~~
5. ~~Checkpoint E - Deploy the application~~ (HOSTED IN Heroku)
6. ~~Checkpoint F (optional - bonus points) - File compression~~ (Image Compression done 'jpg', 'png', 'jpeg', 'gif', 'raw' -> '.jpg')

## To Do

- Write V2 Proper Readme - Explain Usage, Drawbacks and Limitations.
- Try Compression for specific file formats flac to mp3, every image format to jpeg, maybe pdf to bit more higher compressed version of that.
- Actually use pydantic models, OOPS Concepts, and Proper Naming Standards.
  
