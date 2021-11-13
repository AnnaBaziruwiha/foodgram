# foodgram - продуктовый помощник

### Описание
Проект "foodgram - продуктовый помощник" позволяет пользователям публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Развернутый проект можно посмотреть [здесь](http://abzrwh.co.vu/)

Данные админа:

- email: admin_user@ya.ru
- password: gastronom

### Технологии

- Python 3.9.0

- Django 3.2.8

- gunicorn 20.0.4

- djoser 2.1.0

- nginx 1.19.3

- postgres 12.4

### Ресурсы

**users**: пользователи

**recipes**: рецепты

**ingredients**: ингредиенты

**tags**: теги

**subscriptions**: подписки

**shopping_cart**: список покупок

### Запуск проекта в dev-режиме
- Создайте в корне проекта файл .env и пропишите в нем следующие переменные окружения:
```sh
DB_ENGINE # укажите, какая подсистема хранения будет использоваться
DB_NAME # имя базы данных
POSTGRES_USER # логин для подключения к базе данных
POSTGRES_PASSWORD # пароль для подключения к базе данных
DB_HOST # название сервиса
DB_PORT # порт для подключения к базе данных
```
- Находясь в директории проекта, запустите docker-compose:
```sh
docker-compose up -d --build
```
- Соберите статику проекта в папку static
```sh
docker-compose exec web python manage.py collectstatic
```
- Выполните миграции:
```sh
docker-compose exec web python manage.py migrate
```
- Заполните базу начальными данными
```sh
docker-compose exec web python manage.py shell
>>> from django.contrib.contentfiles.models import ContentFile
>>> ContentFile.objects.all().delete()
>>> quit()

docker-compose exec web python manage.py loaddata fixtures.json
```
- Создайте суперпользователя
```sh
docker-compose exec web python manage.py createsuperuser
```
### Контакты
Еще больше моих проектов ищите [тут](https://github.com/AnnaBaziruwiha)

Предложения и пожелания пишите [сюда](abaziruwiha@gmail.com)

Мой [linkedin](https://www.linkedin.com/in/annabaziruwiha/)

