# Docker Wagtail starter



Simple container to run wagtail.
- Python 3
- Wagtail:latest

### Usage

Clone this repo. If you have a wagtail project already, clone into the repo root eg ```./mysite```

If you are starting a new site:

Start the containers

``` docker-compose up -d```

SSH to the web container

``` docker exec -it [web container name] /bin/bash ```

Create app with wagtail@

``` wagtail start mysite```

Then proceed as per the wagtail docs:

##### Create the database
By default, this would create an SQLite database file within the project directory.

```python manage.py migrate```

##### Create an admin user #####

```python manage.py createsuperuser```

##### Run the development server

```python manage.py runserver 0.0.0.0:8000```

Your site is now accessible at 0.0.0.0:8000 (or watever ip your docker is set to), with the admin backend available at http://localhost:8000/admin/.

[Read more on the wagtail docs](http://docs.wagtail.io/en/v1.13.1/)

*you may need to run ```   sudo chown -R $USER:$USER . ``` if you create a wagtail project from within docker
