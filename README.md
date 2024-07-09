# API сервис по управлению менторством.

## Техническое задание:

Создать api приложение на Django с использованием DRF по управлению менторством

## Требования

API должен принимать запросы по следующим адресам:

1. `api/registration` - создание нового пользователя.
2. `api/login` - авторизация пользователя.
3. `api/user/list` - список пользователей.
4. `api/user/<id>` - информация о пользователе.
5. `api/logout` - выход пользователя.

Аутентификация должна быть реализована через djangorestframework-simplejwt.

При регистрации обязательными параметрами являются - логин, пароль. Необязательным - номер телефона, e-mail.
В п.3 присылать информацию по логину и принадлежности к менторам.
К адресам из п.3, п.4 и п.5 должен быть доступ у всех авторизованных пользователей.
п.4 показывать пароль и иметь возможность изменить любое значение только самого себя.
п.4 если пользователь является ментором, то нужно дополнительно присылать список логинов пользователей, для которых он является ментором.
п.4 если у пользователя есть ментор(может быть только один), то присылать логин ментора.


# Реализация.

## Стэк: Django, DRF, PostgreSQL, Cryptography, drf-yasg, docker, djangorestframework-simplejwt

## Запуск:
1. Клонировать проект.
2. Переименовать файл `env.example` в `.env`.
3. В файле `.env` указать данные для подключения PostgreSQL, Djnago secret key и biary code. Biary code нужен для кастомного шифрования пароля.
4. Из корня проекта запустить команду `docker-compose build --no-cache && docker-compose up`.

## Решения:
1. При написании API использовал [Django Styleguide](https://github.com/HackSoftware/Django-Styleguide?tab=readme-ov-file#apis--serializers).
2. В качестве подхода для реализации разных сериализаторов на основе роли использовал [фабрику сериализаторов](https://github.com/mrPechen/RS_template/blob/main/src/api/serializers/factories.py). Выбрал такой подход с учетом возможного расширения ролей.
3. Для избежания нарушения принципа DRY создал 2 базовых сериализатора:
 - [Выдача пароля](https://github.com/mrPechen/RS_template/blob/main/src/api/serializers/base_serializers/base_get_serializer_conf.py) - Перед инициализацией сериализатора проверяет кто делает запрос, и на основе этого при ответе возвращает пароль, либо нет. От этого сериализатора наследуются те сериализаторы, в которых должно содержаться поле `password`.
 - [Валидация данных](https://github.com/mrPechen/RS_template/blob/main/src/api/serializers/base_serializers/base_patch_serializer_conf.py) - Валидирует номер телефона, проверяет уникальность логина и валидирует пароль. От этого сериализатора наследуются сериализаторы, которые на вход принимают эти параметры.
4. Использовал [signals](https://github.com/mrPechen/RS_template/blob/main/src/api/signals.py), чтобы при создании нового пользователя автоматически указать ему роль User.
5. Для реализации условия `показывать пароль` использовал библиотеку `cryptography`. С помощью этой библиотеки реализовал 2 метода в [модели Account](https://github.com/mrPechen/RS_template/blob/main/src/api/models.py). Метод `set_encrypted_password` шифрует сырой пароль пользователя на основе бинарного ключа из файла `.env`. Метод `get_decode_password` дешифрует пароль, позволяя отправить пользователю его пароль.

## Endpoints:

1. `http://127.0.0.1:8000` - Swagger документация.
2. `http://127.0.0.1:8000/api/registration` - Post запрос. Регистрация нового пользователя. Принимает параметры такого вида `{"username": "user", "password": "password", "phone": "71234567891", "email": "example@email.com"}`. Поля phone и email необязательные.
3. `http://127.0.0.1:8000/api/login` - Post запрос. Аутентификация пользователя. Принимает параметры такого вида `{"username": "user", "password": "password"}`. В ответ вернет Bearer токены `{"refresh": "eyJhbGciOiJIUzI1NiIsInR...", "access": "eyJhbGciOiJIUzI1NiIsInR5..."}`.
4. `http://127.0.0.1:8000/api/user/list` - Get запрос. Для доступа требуется Bearer access token. В ответ возвращает список всех пользователей.
5. `http://127.0.0.1:8000/api/user/<id>` - Get запрос. Для доступа требуется Bearer access token. В ответ возвращает информацию о пользователе.
6. `http://127.0.0.1:8000/api/user/<id>` - Patch запрос. Редактирование данных пользователя. Для доступа требуется Bearer access token. Принимает параметры такого вида `{"username": "user", "password": "password", "phone": "71234567891", "email": "example@email.com", "role": "user/mentor", "mentored_users": [1, 2, 3]}`. Все поля являются необязательными.
7. `http://127.0.0.1:8000/api/logout` - Post запрос. Выход из аккаунта. Для доступа требуется Bearer access token. Принимает параметры такого вида `{"refresh": "eyJhbGciOiJIUzI1NiIsInR..."}`.


