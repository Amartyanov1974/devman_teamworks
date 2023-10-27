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
