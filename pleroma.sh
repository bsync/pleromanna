#!/bin/sh
   #mkdir -p /code/s3d
   #s3fs pleromabiblechurch /code/s3d -o umask=033,uid=1000,gid=1000
   exec gunicorn -c python:gconfig pleromanna.wsgi
