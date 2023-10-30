# Devman Teamworks
Проект создан для автоматизация формирования проектных групп и улучшения оповещения студентов о старте учебных проектов.

### Как установить
Для запуска вам понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Создайте env-файл в который будете вносить все переменные окружения

Создайте базу данных:

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```
Создайте суперпользователя
```sh
python3 manage.py createsuperuser
```

### Запуск бота
Для запуска бота management command `./manage.py run_bot`
#### Переменные окружения
`TG_BOT_TOKEN` = указать токен бота

### Генерация случайных студентов для проверки формирования команд
```python3 ./manage.py gen```

### Загрузка студентов и проект-менеджеров
Для загрузки из JSON-файла используйте команду:

```python3 ./manage.py load```

Формат файла допишу в readme, а наши данные уберу.

### Переменные окружения для создания и управления рабочими досками в Trello
После создания рабочего пространства в [Trello](https://trello.com) cоздаем ключи и токен по [этой инструкции](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/)

`TRELLO_API_KEY`- API ключ к рабочему пространству. <br>
`TRELLO_API_TOKEN` - Токен к рабочему пространству. <br>

Команда генерации рабочих досок в Trello для сформированных рабочих групп:<br>
```python3 ./manage.py gen_trello```

### Переменные окружения для Discord бота
`DISCORD_BOT_TOKEN` - Токен к discord боту([инструкция по получению токена и создания Discord сервера.](https://appmaster.io/ru/blog/bot-discord-kak-sozdat-i-dobavit-na-server) <br>
