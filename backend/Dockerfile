FROM alpine:edge

COPY . .
RUN apk update
RUN apk upgrade
RUN apk add postgresql-client
RUN apk add python3
RUN apk add py3-pip
RUN apk add py3-psycopg2
RUN apk add py3-pydantic
RUN apk add py3-fastapi
RUN apk add py3-sqlalchemy
RUN apk add uvicorn

EXPOSE 8000

CMD ["python3", "./main.py"]
