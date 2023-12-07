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


@app.get("/files")
async def list():
    """
    List all files in the DSK image.
    DSKイメージ内の全ファイルのリストを返します

    Returns:
        StreamingResponse: A streaming response containing the list of files in the DSK image.
    """

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

    def getFilesForDir(targetPath):
        for target in Path(targetPath).glob("**/*"):
            if target.is_file():
                yield target.relative_to(targetPath).as_posix() + "\n"
            if target.is_dir():
                yield target.relative_to(targetPath).as_posix() + "/\n"

    if Path(dskfile_path).is_dir():
        return StreamingResponse(getFilesForDir(dskfile_path), media_type="text/plain")
    elif Path(dskfile_path).is_file():
        dskFile = dsk.DSKImage(dskfile_path)
        dskFile.parse()
        return StreamingResponse(getFiles(dskFile.files), media_type="text/plain")
    else:
        return Response(status_code=404, content="File not found")


async def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir


@app.get("/get/{target:path}")
async def dl(target: str = "", dir=Depends(get_temp_dir)):
    """
    Downloads a file from a DSK image.
    DSKイメージからファイルをダウンロードします

    Args:
        target (str): The path of the file to be downloaded from the DSK image.
        (ex: http://localhost:8000/get/AUTOEXE.BAT , http://localhost:8000/get/include/stdio.h , etc..)

    Returns:
        FileResponse: The downloaded file as a FileResponse object.

    Raises:
        Response: If the file is not found in the DSK image, a 404 response is returned.
    """

    if Path(dskfile_path).is_dir():
        logging.info("Path   : " + dskfile_path)
        logging.info("Target : " + target)

        targetFilePath = Path(dskfile_path) / target
        if not targetFilePath.exists():
            logging.info("File not found")
            return Response(status_code=404, content="File not found")

        return FileResponse(targetFilePath, filename=Path(targetFilePath).name)
    elif Path(dskfile_path).is_file():
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

    else:
        logging.info("File not found")
        return Response(status_code=404, content="File not found")


class dsk_server(object):
    """
    Distribution server for files stored in DSK format image file.
    """

    def start(self, target, host="0.0.0.0", port=8000):
        """
        Start the DSK server.

        Args:
            target: Target path on host or the path to the DSK file.
            host: The host IP address to bind the server to. Default is "0.0.0.0".
            port: The port number to bind the server to. Default is 8000.
        """
        if not Path(target).exists():
            logging.error("Target path not found")
            return

        global dskfile_path
        dskfile_path = target
        uvicorn.run(app, host=host, port=port)


def server():
    fire.Fire(dsk_server)


if __name__ == "__main__":
    server()
