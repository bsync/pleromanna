FROM debian:stretch
LABEL maintainer="james.horine@gmail.com"
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
COPY . /code/
WORKDIR /code/
RUN apt-get update 
RUN apt-get install -y ffmpeg certbot s3fs python3-pip libcurl4-openssl-dev libssl-dev
RUN pip3 install -r /code/requirements.txt
RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail
CMD [ "/code/pleroma.sh" ]
