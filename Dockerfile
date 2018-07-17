FROM python:3.5
ENV PYTHONUNBUFFERED 1
ADD pleroma/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
ADD pleroma /pleroma
WORKDIR /pleroma
EXPOSE 80
CMD gunicorn -b 0.0.0.0:80 manna.wsgi
