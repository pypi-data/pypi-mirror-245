import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, FileResponse, Response

from . import dsk_utils as dsk
from pathlib import Path

import fire
import tempfile

import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
dskfile_path = ""

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

@app.get("/get/{target:path}")
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
    logging.info("DSK File: " + dskfile_path)
    logging.info("Target  : " + target)
    dskFile = dsk.DSKImage(dskfile_path)
    dskFile.parse()

    bytesData = dskFile.getBityesFromFilePath(target)
    if bytesData is None:
        logging.info("File not found")
        return Response(status_code=404, content="File not found")

    with open(dir + "/temp", "wb") as f:
        f.write(bytesData)

    return FileResponse(dir + "/temp", filename=Path(target).name)
    


class dsk_server(object):
    """
    This class represents the startup process of the DSK server.
    """

    def start(self, dskfile, host="0.0.0.0", port=8000):
        """
        Starts the DSK server.

        Parameters:
        - dskfile (str): The path to the DSK file.

        Returns:
        - None
        """
        global dskfile_path
        dskfile_path = dskfile
        uvicorn.run(app, host=host, port=port)

def server():
    fire.Fire(dsk_server)

if __name__ == "__main__":
    server()
