import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, FileResponse

from . import dsk_utils as dsk
from pathlib import Path

import fire
import tempfile

app = FastAPI()

dskfile_path = ""

@app.get("/")
async def root(path:str =""):
    return {"message": dskfile_path}

@app.get("/list")
async def list():
    dskFile = dsk.DSKImage(dskfile_path)
    dskFile.parse()
    return dskFile.files

async def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir

@app.get("/dl/")
async def dl(target:str ="", dir = Depends(get_temp_dir)):
    """
    Downloads a file from a DSK image.

    Args:
        target (str): The path of the file to be downloaded from the DSK image.
        dir: The temporary directory where the downloaded file will be saved.

    Returns:
        FileResponse: The downloaded file as a FileResponse object.

    Raises:
        FileNotFoundError: If the specified file is not found in the DSK image.
    """
    print("DSK File: " + dskfile_path)
    print("Target: " + target)
    dskFile = dsk.DSKImage(dskfile_path)
    dskFile.parse()
    print("parse done")

    bytesData = dskFile.getBityesFromFilePath(target)
    if bytesData is None:
        return {"message": "file not found"}

    with open(dir + "/temp", "wb") as f:
        f.write(bytesData)

    return FileResponse(dir + "\\temp", filename=Path(target).name)
    


class StartUP(object):
    """
    This class represents the startup process of the DSK server.
    """

    def start(self, dskfile):
        """
        Starts the DSK server.

        Parameters:
        - dskfile (str): The path to the DSK file.

        Returns:
        - None
        """
        global dskfile_path
        dskfile_path = dskfile
        uvicorn.run(app, host="0.0.0.0")

def server():
    fire.Fire(StartUP)

if __name__ == "__main__":
    server()
