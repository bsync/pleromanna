import multiprocessing

reload = True
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 
accesslog = '-'
certfile='/run/secrets/site.crt'
keyfile='/run/secrets/site.key'
