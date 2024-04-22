# BUILD FRONTEND
Команда для запуска билда CSS и кастомных стилей для FLOWBITE/TAILWIND
```bash
npx tailwindcss -i ./static/css/style.css -o ./static/css/dist/output.css --watch  # Указываем тейлвинду путь до CSS файла и куда его конфигурировать
```

# BUILD BACKEND 
Активируем окружение и запускаем сервак. Работает на 80 порту.
```bash
venv\Scripts\activate  # Активируем окружение Python
python main.py  # Запускаем сервер
```

# AERICH INIT & MARIADB
Работает по ссылке `mysql://root@localhost:3306/blogo`\
Данная утилита нужна для миграций в базу данных
```bash
aerich init -h  # Инициализируем aerich
aerich init -t main.TORTOISE_ORM  # Инициализируем конфигурационный файл
aerich init-db  # Инициализируем базу
aerich migrate --name init  # Делаем первую миграцию
aerich upgrade  # Обновляемся до последней версии миграций
```

# Структура проекта
```bash
- api  # Отвечает за API сайта
    - __init__  # Импорт всех модулей для более удобной работы
    - modules
- database  # Папка для указания моделей для базы
    - models  # Описываем поля в базе
- frontend_manager  # Папка отвечает за раздачу статики
    - __init__  
    - modules
- migrations   # Папка отвечает за миграции для бд
    - models
- static  # Отвечает за удержание необходимой статики
    - css  # Все стили
    - imgs  # Все картинки
    - scripts  # Весь JS код
- templates  # Отвечает за HTML заготовки для генерации и последующей раздаче в frontend_manager
    - modules
- venv  # Виртуальное окружение Python
- node_modules  # Виртуальное окружение node.js
- main.py  # Основная входная точка приложения
- package.json  # Описывает зависимости JS
- poetry.lock  # Описывает зависимости Python
- tailwind.config.js  # Описывает конфиг для Tailwind
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


# Логика работы приложения
1. Пользователь выполняет запрос
2. FastAPI подхватывает входящий запрос и направляет в один из путей
3. Определенный route обрабатывает этот запрос и выдает ответ, например генерирует статику благодаря Jinja2 и отдает пользователю
4. Дополнительно прописаны API routes, для невидимых запросов
