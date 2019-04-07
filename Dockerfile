FROM python:3.6
LABEL maintainer="james.horine@gmail.com"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev

COPY . /code/
WORKDIR /code/
RUN pip install -r /code/requirements.txt
RUN useradd wagtail
RUN chown -R wagtail /code
USER wagtail

EXPOSE 8000

CMD exec gunicorn pleromanna.wsgi:application --bind 0.0.0.0:8000 --workers 3
