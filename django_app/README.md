# Django Web App

- cd into hospital_register_app
- create the .env file with the credentials for db and django
- cd into ./nginx
- replace "localhost" with the domain name in the file "default.conf"
- cd back (..)
- run the command "docker-compose up -d --build"

#### Populate database:
docker exec -it hospital_register_app-db-1 bash

[winpty docker exec -it hospital_register_app-db-1 //bin//sh  # from Windows machine using GitBash]

mysql -uroot -proot_password hospital_register_db < /tmp/populate_details_and_locations.sql
