# **YAMDB**
**REST API для сервиса YaMDB** — базы данных о фильмах, книгах и музыке.
***
## Описание проекта
Проект сервиса API для YaMDb позволяет собирать отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
***
## **Описание API**
**API для сервиса YaMDb. Позволяет работать со следующими сущностями:**
- **Отзывы:**
  + получить список всех отзывов;
  + создать новый отзыв;
  + получить отзыв по id;
  + частично обновить отзыв по id;
  + удалить отзыв по id.
- **Комментарии к отзывам:**
  + Получить список всех комментариев к отзыву по id;
  + создать новый комментарий для отзыва, получить комментарий для отзыва по id;
  + частично обновить комментарий к отзыву по id;
  + удалить комментарий к отзыву по id.
- **JWT-токен:**
  + Отправление confirmation_code на переданный email;
  + получение JWT-токена в обмен на email и confirmation_code.
- **Пользователи:**
  + Получить список всех пользователей;
  + создание пользователя получить пользователя по username;
  + изменить данные пользователя по username;
  + удалить пользователя по username;
  + получить данные своей учетной записи;
  + изменить данные своей учетной записи.
- **Категории (типы) произведений:**
  + Получить список всех категорий;
  + создать категорию;
  + удалить категорию.
- **Категории жанров:**
  + получить список всех жанров
  + создать жанр;
  + удалить жанр.
- **Произведения, к которым пишут отзывы:**
  + Получить список всех объектов;
  + создать произведение для отзывов;
  + информация об объекте;
  + обновить информацию об объекте;
  + удалить произведение.
***
## **Алгоритм регистрации пользователей**
1. Пользователь отправляет запрос с параметром email на `/auth/email/`.
2. YaMDB отправляет письмо с кодом подтверждения `(confirmation_code)` на адрес `email`.
3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на `/users/me/` и заполняет поля в своём профайле (описание полей — в документации).
***
## **Пользовательские роли**
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песням), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- **Модератор** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.
***
## **Доступные методы:**

### Reviews

`/api/v1/titles/{title_id}/reviews/ (GET, POST)`

`/api/v1/titles/{title_id}/reviews/{review_id}/ (GET, PATCH, DELETE)`

### Comments

`/api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST)`

`/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (GET PATCH, DELETE)`

### Auth

`/api/v1/auth/token/ (POST)`

`/api/v1/auth/email/ (POST)`

### Users 

`/api/v1/users/ (GET, POST)`

`/api/v1/users/{username}/ (GET, PATCH, DELETE)`

`/api/v1/users/me/ (GET, PATCH)`

### Categories

`/api/v1/categories/ (GET, POST)`

`/api/v1/categories/{slug}/ (DELETE)`

### Genres

`/api/v1/genres/ (GET, POST)`

`/api/v1/genres/{slug}/ (DELETE)`

### Titles

`/api/v1/titles/ (GET, POST)`

`/api/v1/titles/{titles_id}/ (GET, PATCH, DELETE)`

***
## Авторы: [Владимир Свириденко](https://github.com/Star-memory), [Пётр Богомолов](https://github.com/IshiiragiIshi), [Фархад Гараев](https://github.com/PARTYNEXTDOORS).
***
## Стэк технологий
- [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
+ [Django Rest Framework](https://www.django-rest-framework.org/)
* [Simple-JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Запуск проекта в dev-режиме
- Клонировать репозиторий и перейти в него в командной строке:
```
'git clone git@github.com:PARTYNEXTDOORS/api_final_yatube.git'
```
```
'cd api_final_yatube'
```
- Cоздать и активировать виртуальное окружение:
```
'python -m venv venv'
```
```
'source venv/Scripts/activate'
```
- Установить зависимости из файла requirements.txt:
```
'python -m pip install --upgrade pip'
```
```
'pip install -r requirements.txt'
```
- Выполнить миграции:
```
'python manage.py migrate'
```
- Запустить проект на локальном сервере:
```
'python manage.py runserver'
```
- Для загрузки тестовых данных из csv-файлов выполнить команду:
```
python manage.py csv
```
[Документация доступна по адресу](http://127.0.0.1:8000/redoc)