#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/11/8 08:53
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/uOcaKQkNROTXqFuKA3hznQ

docker run --name old-oneapi \
  -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v /root/one-api:/data \
  justsong/one-api

docker run --name Xoneapi \
  -d --restart always \
  -p 39001:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:chatllmchatllm@tcp(host.docker.internal:3306)/oneapi" -e TZ=Asia/Shanghai \
  -v /root/data/xapi:/data \
  justsong/one-api

docker pull calciumion/new-api:latest
docker run --name vip \
  -d --restart always \
  -p 39002:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:chatllmchatllm@tcp(host.docker.internal:3306)/oneapi" -e TZ=Asia/Shanghai \
  -v /root/data/xapi:/data \
  calciumion/new-api:latest

docker run --name chat \
  -d -p 3004:3000 \
  -e PROXY_URL=http://127.0.0.1:39001 \
  yidadaa/chatgpt-next-web


# 代理服务
docker run --name aiapi \
  -d --restart always \
  -p 39003:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:chatllmchatllm@tcp(host.docker.internal:3306)/aiapi" -e TZ=Asia/Shanghai \
  -v /root/data/aiapi:/data \
  calciumion/new-api:latest