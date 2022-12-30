# 🛠 Educational project. 
Online cinema. API can give information about movies in the database and about each specific movie, the application has an admin panel and full text search based on Elasticsearch which loads by ETL process.

The following tools were used in the backend part of the project:
- Python 3.10
- Django 3.2
- Elasticsearch 7.7
- Redis 6

The infrastructure part used:
- PostgreSQL
- Docker
- Nginx


# 🚀 Project installation

Install Docker and docker-compose:
```sh
sudo apt-get update
sudo apt install docker.io 
sudo apt-get install docker-compose-plugin
```
Clone repository:
```sh
git clone git@github.com:gufin/new_admin_panel_sprint_3.git
```
When deploying to a server, you need to create a file with the values of the .env variables in the docker_compose folder.
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs
DEBUG=False

REDIS_HOST=redis
REDIS_PORT=6379

ELASTIC_HOST=elastic
ELASTIC_PORT=9200
ELASTIC_USER=movies_admin
ELASTIC_PASSWORD=movies_admin
```
The `your_postgres_user` and `your_postgres_user_password` fields need to fill in with your PostgreSQL database connection data. To generate the SECRET_KEY value, you can use the command: 
```sh
openssl rand -hex 32
```
When running on a server, you need to add the address of your server to the ALLOWED_HOSTS variable in the backend/foodgram/settings.py file.

##### 🐳 Running Docker containers
When you first start from the infra directory, you need to run the command:
```sh
sudo docker-compose up -d --build
```
On subsequent launches, the --build key can omit.

Create django superuser:
```sh
sudo docker-compose exec web python manage.py createsuperuser
```
Load ingredient data:
```sh
sudo docker-compose exec web python manage.py loaddata data.json
```
[Api documentation](http://127.0.0.1:8080/) 

[Admin panel](http://127.0.0.1:8000/admin/) 

[ElasticSearch API](http://127.0.0.1:9200) 

# :smirk_cat: Author
Drobyshev Ivan

