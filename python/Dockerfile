FROM python:3.8.0-alpine3.10

LABEL Name=python Version=0.0.1
EXPOSE 3000

WORKDIR /app
ADD ./src /app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
 
CMD ["python3", "-m", "app"]

