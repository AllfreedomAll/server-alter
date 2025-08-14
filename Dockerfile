FROM python:3.9.12-alpine3.15

MAINTAINER "lingguo@outlook.com"

WORKDIR /data/server-alter/

COPY requirements.txt ./

RUN apk add gcc g++ make git python3-dev mariadb-dev musl-dev libffi-dev jpeg-dev zlib-dev libxml2-dev libxslt-dev

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "start.sh"]
CMD ["sh", "/data/server-alter/start.sh"]
