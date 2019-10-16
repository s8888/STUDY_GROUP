# Flask best practice

Topic: Flask, flask-restplus, cookiecutter, docker-compose

## 執行

1. jpyter notebook 環境確認

    ```bash
    docker-compose up -d
    docker-compose logs
    ```

    進入 jupyter notebook [localhost:8888](http://localhost:8888)

2. API 服務確認

    ```bash
    # in host
    # sample_code/sample/deploy/sample/
    bash up.sh
    ```

    進入 [localhost:6001](http://localhost:6001) 確認有出現 Swagger UI

## 確定 docker 版本

```bash
docker version
```

```txt
Client: Docker Engine - Community
 Version:           18.09.2
 API version:       1.39
 Go version:        go1.10.8
 Git commit:        6247962
 Built:             Sun Feb 10 04:12:39 2019
 OS/Arch:           darwin/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          18.09.2
  API version:      1.39 (minimum version 1.12)
  Go version:       go1.10.6
  Git commit:       6247962
  Built:            Sun Feb 10 04:13:06 2019
  OS/Arch:          linux/amd64
  Experimental:     true
```

## 確定 docker-compose 版本

```bash
docker-compose version
```

```txt
docker-compose version 1.23.2, build 1110ad01
docker-py version: 3.6.0
CPython version: 3.6.6
OpenSSL version: OpenSSL 1.1.0h  27 Mar 2018
```
