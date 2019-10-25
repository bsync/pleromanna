FROM debian:stretch
LABEL maintainer="james.horine@gmail.com"
RUN apt-get update 
RUN apt-get install -y ffmpeg certbot s3fs python3-pip libcurl4-openssl-dev libssl-dev
RUN useradd wagtail
COPY --chown=wagtail requirements.txt /home/wagtail/
RUN pip3 install -r /home/wagtail/requirements.txt
COPY --chown=wagtail . /home/wagtail/
USER wagtail
WORKDIR /home/wagtail
CMD ["gunicorn", "-c", "gconfig.py", "pleromanna.wsgi"]
