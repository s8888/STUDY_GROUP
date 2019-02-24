# Flask best practice
Topic: Flask, gunicorn, nginx

### 執行
```
docker-compose up -d
docker-compose logs
```
進入 jupyter notebook [localhost:8888](http://localhost:8888)  

### 確定 docker 版本
```
docker version
```
<pre>
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
</pre>

### 確定 docker-compose 版本
```
docker-compose version
```
<pre>
docker-compose version 1.23.2, build 1110ad01
docker-py version: 3.6.0
CPython version: 3.6.6
OpenSSL version: OpenSSL 1.1.0h  27 Mar 2018
</pre>
