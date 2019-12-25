Traefik V2.0 介紹

環境需求: 
1. docker
2. docker-compose

used images: 
1. traefik:v2.0
2. containous/whoami

執行確認
example0 資料夾下執行
docker-compose up -d

正常的話
8080 port 會有 Dashboard
curl -H Host:whoami.docker.localhost http://127.0.0.1 會有訊息回傳


官網
https://docs.traefik.io/

