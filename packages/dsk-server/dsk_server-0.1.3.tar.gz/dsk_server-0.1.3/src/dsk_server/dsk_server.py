import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse, FileResponse, Response

from . import dsk_utils as dsk
from pathlib import Path

import fire
import tempfile
import socket

import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()
dskfile_path = ""


@app.get("/list")
async def list():
    dskFile = dsk.DSKImage(dskfile_path)
    dskFile.parse()
    return dskFile.files


@app.get("/files")
async def list():
    def getFiles(files: dict):
        dir: str
        for dir in files.keys():
            for file in files[dir]:
                if file["Attribute"]["VolumeLabel"]:
                    continue
                if file["Attribute"]["Directory"]:
                    continue
                if dir == "/":
                    yield file["FileName"].decode(
                        encoding="ascii"
                    ).rstrip() + "." + file["Extension"].decode(
                        encoding="ascii"
                    ).rstrip() + "\n"
                else:
                    yield dir.replace(" ", "") + "/" + file["FileName"].decode(
                        encoding="ascii"
                    ).rstrip() + "." + file["Extension"].decode(
                        encoding="ascii"
                    ).rstrip() + "\n"

    dskFile = dsk.DSKImage(dskfile_path)
    dskFile.parse()
    return StreamingResponse(getFiles(dskFile.files), media_type="text/plain")


async def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir


@app.get("/get/{target:path}")
async def dl(target: str = "", dir=Depends(get_temp_dir)):
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
        logging.info("Starting DSK server {}".format(socket.gethostbyname(host)))
        uvicorn.run(app, host=host, port=port)


def server():
    fire.Fire(dsk_server)


if __name__ == "__main__":
    server()
