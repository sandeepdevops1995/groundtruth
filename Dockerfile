FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /atco-groundtruth

ADD . /atco-groundtruth

ENV PATH /root/.local/bin:$PATH

RUN apt update -y && apt upgrade -y && apt install -y vim

RUN apt install -y make

RUN python -m pip install pipenv

RUN pip install coverage

COPY ./Pipfile Pipfile

RUN make install

CMD [ "make", "run-docker"]