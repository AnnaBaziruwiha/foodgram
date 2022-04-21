# foodgram - groceries assistant

### Description
This project currently only supports Russian language.
The "foodgram" project helps its users to publish recipes, subscribe to other users' publications, add recipes to favorites(«Избранное»), and download the shopping list that contains all the ingredients from the favorited recipes.

### Technologies

- Python 3.9.0

- Django 3.2.8

- gunicorn 20.0.4

- djoser 2.1.0

- nginx 1.19.3

- postgres 12.4

### Resources

**users**

**recipes**

**ingredients**

**tags**

**subscriptions**

**shopping_cart**

### Deploy the project in developer mode
- Create the .env file in the root of the project and fill it with the following data:
```sh
DB_ENGINE # укажите, какая подсистема хранения будет использоваться
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к базе данных
DB_HOST # название сервиса
DB_PORT # порт для подключения к базе данных
```
- Run docker-compose in the project's directory:
```sh
docker-compose up -d --build
```
- Collect the project's static files in the static folder
```sh
docker-compose exec web python manage.py collectstatic
```
- Make migrations:
```sh
docker-compose exec web python manage.py migrate
```
- Fill the database with initial data
```sh
docker-compose exec web python manage.py shell
>>> from django.contrib.contentfiles.models import ContentFile
>>> ContentFile.objects.all().delete()
>>> quit()

docker-compose exec web python manage.py loaddata fixtures.json
```
- Create a superuser
```sh
docker-compose exec web python manage.py createsuperuser
```
### Contacts
Check out more of my projects [here](https://github.com/AnnaBaziruwiha)

You can send suggestions and requests to [this address](abaziruwiha@gmail.com)

My [linkedin](https://www.linkedin.com/in/annabaziruwiha/)

