# dsk-server

FAT12形式のDSKファイルに含まれるファイルをダウンロードできるサーバアプリケーションです

### インストール

```
pip install dsk-server
```

### Usage

```
NAME
    dsk-server start - Start the DSK server.

SYNOPSIS
    dsk-server start DSKFILE <flags>

DESCRIPTION
    Start the DSK server.

POSITIONAL ARGUMENTS
    DSKFILE

FLAGS
    -h, --host=HOST
        Default: '0.0.0.0'
    -p, --port=PORT
        Default: 8000
```

### API

サーバを起動して、以下を参照ください

```
http://127.0.0.1/docs
```
