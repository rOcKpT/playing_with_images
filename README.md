 Imanager - Image manager
Welcome to the Imanager, to setup this project you need to do following steps.
### Docker
Inside the root of the project do the following commands.

`docker-compose build`

`docker-compose up`

###Database
The container are running, but if you go to http://0.0.0.0:8000 we can see that an error related with the database occours, that's because with need to do some migraitons. Just run these command

`docker-compose exec web python manage.py migrate`

Now if you go back to the http://0.0.0.0:8000, you can see the login page and the project is ready to be used, just register in the site and you're free to some image management.

###Admin Access
To access the django admin, you need to create a superuser, you can do that with the following command:

`docker-compose exec web python manage.py createsuperuser`