<div style="text-align: center;">
  <h1>Flaskter</h1>  
<h2>Сервис микроблогов. </h2>
</div>

| ORM        | База данных | Фреймворк | API           | Документация | Контейнер      | Тесты                      | Линтеры                    | Веб   | WSGI     | Python | Миграции |
|------------|-------------|-----------|---------------|--------------|----------------|----------------------------|----------------------------|-------|----------|--------|----------|
| SQLAlchemy | Postgresql  | Flask     | Flask Restful | Flasgger     | Docker-compose | pytest,  | black, isort, mypy, flake8 | nginx | gunicorn | 3.12   | alembic  |

<div style="text-align: center;">
<h3>Запуск</h3>
</div>

`docker-compose up --build`

<div style="text-align: center;">
<h3>Документация</h3>
</div>

`/apidocs`

<div style="text-align: center;">
<h3>Техническое задание</h3>
</div>
Реализовать бэкенд сервиса микроблогов.
Описание поведения
Для корпоративного сервиса микроблогов необходимо реализовать бэкенд
приложения. Поскольку это корпоративная сеть, то функционал будет урезан
относительно оригинала. Как правило, описание сервиса лучше всего дать
через функциональные требования, то есть заказчик формулирует простым языком, что система должна уметь делать. Или что пользователь хочет делать
с системой. И вот что должен уметь делать наш сервис:

Функциональные требования:
1. Пользователь может добавить новый твит.
2.  Пользователь может удалить свой твит.
3.  Пользователь может зафоловить другого пользователя.
4.  Пользователь может отписаться от другого пользователя.
5.  Пользователь может отмечать твит как понравившийся.
6. Пользователь может убрать отметку «Нравится».
7. Пользователь может получить ленту из твитов отсортированных в
порядке убывания по популярности от пользователей, которых он
фоловит.
8. Твит может содержать картинку.
Заметим, что требования регистрации пользователя нет: это корпоративная
сеть и пользователи будут создаваться не нами. Но нам нужно уметь отличать
одного пользователя от другого.

<div style="text-align: center;">
<h3>Endpoints</h3>
</div>

|    | **метод** | **роут**               | **описание**                                                                                                                                                            |
|----|-----------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1  | post      | api/tweets             | Запросом на этот endpoint пользователь будет создавать новый твит.<br>Бэкенд будет его валидировать и сохранять в базу.<br>В ответ должен вернуться id созданного твита |
| 8  | get       | /api/tweets            | Пользователь может получить ленту с твитами. В ответ должен вернуться json со списком твитов для ленты этого<br>Пользователя.                                           |
| 3  | delete    | /api/tweets/<id>       | В этом endpoint мы<br>должны убедиться, что пользователь удаляет именно свой собственный твит. В ответ должно вернуться сообщение о статусе операции.                   |
| 4  | post      | /api/tweets/<id>/likes | Пользователь может поставить отметку «Нравится» на твит. В ответ должно вернуться сообщение о статусе операции.                                                         |
| 5  | delete    | /api/tweets/<id>/likes | Пользователь может убрать отметку «Нравится» с твита. В ответ должно вернуться сообщение о статусе операции.                                                            |
| 6  | post      | /api/users/<id>/follow | Пользователь может зафоловить другого пользователя. В ответ должно вернуться сообщение о статусе операции.                                                              |
| 7  | delete    | /api/users/<id>/follow | Пользователь может убрать подписку на другого пользователя. В ответ должно вернуться сообщение о статусе операции.                                                      |
| 9  | get       | /api/users/me          | Пользователь может получить информацию о своём профиле:                                                                                                                 |
| 2  | post      | /api/medias            | Endpoint для загрузки файлов из твита. Загрузка происходит через<br>отправку формы. В ответ должен вернуться id загруженного файла.                                     |
| 10 | get       | /api/users/<id>        | Пользователь может получить информацию о произвольном профиле по его<br>Id:                                                                                             |

8. Скриншоты

<div style="text-align: center;">
<h3>Покрытие тестами</h3>
</div>
