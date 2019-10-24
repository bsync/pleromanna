import multiprocessing

reload = True
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 
#workers = 1 
accesslog = '-'
certfile='/code/ssl/crt'
keyfile='/code/ssl/key'
