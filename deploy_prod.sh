#!/usr/bin/env bash
# git clone http://gitlab-ci-token:5pW_dfANjs-gD4aHPoXu@gitlab.testbird.com/vpn/sonic_secure_x2.git
project=server-alter
docker_path=/data/server-alter
ver=$1
ver=${ver:-"0.0.1"}
echo "will deploy ver: $ver"
sudo docker build  . -t woaini2021/${project}:${ver}
sudo docker push woaini2021/${project}:${ver}
sudo docker pull woaini2021/${project}:${ver}
sudo docker stop ${project}
sudo docker rm -f ${project}


sudo docker run -itd --name ${project} --net host --env site_env=prod -p 8000:8000 -v /data/docker_shared/mix/prod/assets:${docker_path}/assets -v /data/docker_shared/mix/prod/logs:${docker_path}/logs -v /data/docker_shared/prod/prometheus:${docker_path}/prometheus --restart always woaini2021/${project}:0.0.1

