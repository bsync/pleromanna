FROM python:3.5
ENV PYTHONUNBUFFERED 1
WORKDIR /pleroma
ADD pleroma/requirements.txt /pleroma/requirements.txt
RUN pip install -r /pleroma/requirements.txt
ADD pleroma /pleroma
EXPOSE 80
CMD python manage.py migrate; gunicorn -b 0.0.0.0:80 pleroma.wsgi
