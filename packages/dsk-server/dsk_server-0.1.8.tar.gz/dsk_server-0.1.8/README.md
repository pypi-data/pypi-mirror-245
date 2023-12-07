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
    dsk-server start [DSKFILE | PATH] <flags>

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

例1：
DSKイメージ内のファイルをホスティングします
```
$ dsk-server start ./MSXDSK.DSK
```

例2：
ホスト上の指定パス内のファイルをホスティングします
```
$ dsk-server start ./work_dir
```


### API

サーバを起動して、以下を参照ください

```
http://127.0.0.1/docs
```


