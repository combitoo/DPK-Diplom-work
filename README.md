# Сборка стилей Tailwind
Команда для запуска билда CSS и кастомных стилей для Tailwind
```bash
npx tailwindcss -i ./static/css/style.css -o ./static/css/dist/output.css --watch
```

# Запуск сервера 
Активируем окружение и запускаем сервер. Работает на 80 порту.
```bash
venv\Scripts\activate
python main.py
```

# AERICH инициализация & База данных
Дефолтная ссылка для базы `mysql://root@localhost:3306/blogo`\
Миграции:
```bash
aerich init -h  # Инициализируем aerich
aerich init -t main.TORTOISE_ORM  # Инициализируем конфигурационный файл
aerich init-db  # Инициализируем базу
aerich migrate --name init  # Делаем первую миграцию
aerich upgrade  # Обновляемся
```

# Используемые технологии
На стороне сервера используется:
1. Python
2. FastAPI - основной API wrapper
3. Tortoise-orm - ORM для работы с БД
4. Aerich - миграции
5. Jinja2 - Template движок
6. Uvicorn - для запуска веб-сервера
7. Passlib - для работы с паролями
8. Fastapi_Login - для авторизации пользователя

На стороне фронтенда используется:
1. node.js
2. Tailwind - стили
3. Jinja2 - Template движок
