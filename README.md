# cldwry_hk_2k22

The WEB-APP is [ACTIVE HERE](https://drive-cldwry-2k22.herokuapp.com/)
The CLI-APP doc is [HERE](https://github.com/Joel-Marc/cldwry_hk_2k22/blob/master/CLI_APP/README.md)

## Features of WEB-APP

- UPLOAD one or More File/s At a time
- Download Files (shows preview of the file too)
- Re-Name Files (can be exact name with file extention or with out one)
- Delete Files
- Share Files
- Go b/w Users

All operations are straight Forward

> If it asks for authentication use either of these usr:pass pairs {"stan": "sword", "joe": "win", "may": "spi"}

## Drawbacks and Limitations WEB-APP

- I have not been able to implement checkpoint A (Authentication and session management) (YET!!) to implement session management ive divided user sessions/repos as folders under the folder ./fil. So, To Go between Users ive put anchor tags.

The blob storage application should have the following features:

1. Checkpoint A - User authentication (Not done properly) and session management (Technically done that) (will improve to standards)
2. ~~Checkpoint B - Implementation of the blob storage server~~
3. ~~Checkpoint C - Client application (CLI/ web based) for file upload, download, rename and delete~~
4. ~~Checkpoint D - User based access control on who can access the files~~
5. ~~Checkpoint E - Deploy the application~~
6. Checkpoint F (optional - bonus points) - File compression (will try)

## To Do

- Write V2 Proper Readme - Explain Usage, Drawbacks and Limitations.
- ~~Build a CLI based Application to access api~~
- Try Compression for specific file formats flac to mp3, every image format to jpeg, maybe pdf to bit more higher compressed version of that.
- Make Login and Authentication and proper session management Possible -> Store hashed pass and check (Using MongoDB or SQLite) -> if time permits Fastapi Oauth or token based authentication and session management.
- Read throught FastAPI docs and actually use pydantic models, OOPS Concepts.
- Database to be included for filenames and their hash (so multiple same files can be stored) and for user authentication.(Currently a fake_db a dictionary is being used)
  