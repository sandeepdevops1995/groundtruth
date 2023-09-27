FROM python:3.8

ENV TZ=Asia/Kolkata

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /atco-groundtruth

ADD . /atco-groundtruth

ENV PATH /root/.local/bin:$PATH

RUN apt update -y && apt upgrade -y && apt install -y vim

RUN apt install -y make

RUN python -m pip install pipenv

RUN pip install coverage

#uwsgi setup
RUN apt-get install -y libpcre3 libpcre3-dev libssl-dev
RUN CFLAGS="-I/usr/local/opt/openssl/include" LDFLAGS="-L/usr/local/opt/openssl/lib" UWSGI_PROFILE_OVERRIDE=ssl=true

COPY ./Pipfile Pipfile

RUN make install  -o reset-local-settings

CMD [ "make", "run"]