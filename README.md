# Описание проекта «API для Yatube»
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

# Используемые технологии:
Python 3.9.13, Django 3.2.16, DjangoRestFramework 3.12.4, simpleJWT 4.7.2

# Установка
Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:LevKorobeinikov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

В проекте находятся тестовые данные для заполнения Базы Данных /static/data. Для заполнения БД необходимо пеерйти в директорию с dbsqlite3 выполнить команду для подкоючения к ней:
```
sqlite3 db.sqlite3
```
Для загрузки тестовых данных выполните комманды:
```
.mode csv
.separator ","
.import static/data/category.csv reviews_category
.import static/data/comments.csv reviews_comment
.import static/data/genre_title.csv reviews_title_genre
.import static/data/genre.csv reviews_genre
.import static/data/review.csv reviews_review
.import static/data/titles.csv reviews_title
.import static/data/users.csv reviews_yamdbuser
```

Запустить проект:

```
python manage.py runserver
```

# Алгоритм регистрации пользователей

1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).

# Пользовательские роли

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладет правами администратора (admin)

# Примеры запросов к API
Регистрация POST:
```
/api/v1/auth/signup/
```
Пример запроса:
```
{
  "email": "user@example.com"
  "username": "^w\\Z"
}
```
Пример ответа:
```
{
  "email": "string",
  "username": "string"
}
```

Добавление нового отзыва POST:
```
/api/v1/titles/{title_id}/reviews/
```
Пример запроса:
```
{
  "text": "string",
  "score": integer
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


Добавление комментария к отзыву POST:
```
/api/v1/titles/{title_id}/reviews/{reviews_id}/comments/
```
Пример запроса:
```
{
  "text": "string"
}
```
Пример ответа:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


# Используемые технологии:
Python 3.9.13, Django 3.2.16, DjangoRestFramework 3.12.4, simpleJWT 4.7.2

# Авторы
[Лев Коробейников](https://github.com/LevKorobeinikov)

[Максим Журавлев](https://github.com/MaxMen00)

[Наиль Мансуров](https://github.com/NailMansurov)
