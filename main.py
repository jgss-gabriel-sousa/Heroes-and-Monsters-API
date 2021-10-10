from fastapi import FastAPI, HTTPException
import random
import os
from fastapi.responses import FileResponse

app = FastAPI()

directories = [
    "data/monster/",
    "data/spell/",
    "data/class/",
    "data/general/",
]


@app.get("/")
async def full_index():
    files = {}

    for i in directories:
        dirFiles = os.listdir(i)
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
        print(Type)
        dirFiles = os.listdir("data/"+Type)
        dirFiles = [j[:-5] for j in dirFiles] #without file format
        dirFiles.sort()
        return dirFiles
    except:
        raise HTTPException(status_code=404, detail="404: Item not found")


@app.get("/{Type}/id:{id_value}")
async def return_data_by_id(Type: str, id_value: int):
    path = "data/"+Type+"/"
    try:
        files = os.listdir(path)
    except:
        raise HTTPException(status_code=404, detail="404: Item not found")

    if(id_value < len(files)):
        path += files[id_value]
        return FileResponse(path)
    else:
        raise HTTPException(status_code=404, detail="404: Item not found")
