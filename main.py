from fastapi import FastAPI, HTTPException
import random, os
import jsonChecker
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

directories = [
    "data/monster/",
    "data/spell/",
    "data/class/",
    "data/general/",
    "data/items/weapons/",
]


@app.get("/")
async def full_index():
    files = {}

    for i in directories:
        dirFiles = os.listdir(i)

        for j in dirFiles: #dnot list folders
            if "." not in j:
                dirFiles.remove(j)

        #for j in dirFiles:
        #    jsonChecker.checkFile(j,i)

        dirFiles = [j[:-5] for j in dirFiles] #without file format
        dirFiles.sort()

        files[i[5:-1]] = dirFiles #without images folder

    return files


@app.get("/query-{name}")
async def return_data_by_name(name: str):
    found = False
    name = name.lower()
    name += ".json"

    for i in directories:
        folderFiles = os.listdir(i)

        if name in folderFiles:
            path = i+name
            found = True
            break

    if found:
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="404: Item not found")


@app.get("/index-{Type}")
async def returns_the_index_of_a_type(Type: str):
    try:
        dirFiles = os.listdir("data/"+Type)
        dirFiles = [j[:-5] for j in dirFiles] #without file format
        dirFiles.sort()
        return dirFiles
    except:
        raise HTTPException(status_code=404, detail="404: Item not found")


@app.get("/{Type}/{id_value}")
async def return_data_by_id(Type: str, id_value: int):
    path = "data/"+Type+"/"
    try:
        files = os.listdir(path)
        files.sort()
    except:
        raise HTTPException(status_code=404, detail="404: Item not found")

    if(id_value < len(files) and id_value >= 0):
        path += files[id_value]
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="404: Item not found")
