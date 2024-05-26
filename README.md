 ## Техническое задание

Реализовать бэкенд для работы со складом рулонов металла.

DTO рулона:
- Id;
- длина;
- вес;
- дата добавления;
- дата удаления.

## Стек
- Python
- FastAPI
- PostgreSQL
- SQLalchemy
- Uvicorn
- Alembic
- Poetry
- pytest-asyncio

## Функциональность проекта

1. **POST /coil**

Добавление нового рулона на склад. Длина и вес обязательно должны быть
заданы.
В случае успеха возвращает назначенный id рулона.

2. **DELETE /coil**

Удаление рулона с указанным id со склада.

3. **GET /coil.**

Получение списка рулонов со склада по указанному диапазону id / веса / длины /
даты добавления / даты удаления со склада. На вход принимается комбинация диапазонов для 
фильтрации, если одна из границ диапазона не задана, то фильтрация произойдет по одной границе.

5. **GET /coil/stats**

Получение статистики по рулонам за определённый период:
- количество добавленных рулонов; 
- количество удалённых рулонов; 
- средняя длина, вес рулонов, находившихся на складе в этот период; 
- максимальная и минимальная длина и вес рулонов, находившихся на складе
в этот период; 
- суммарный вес рулонов на складе за период; 
- максимальный и минимальный промежуток между добавлением и удалением
рулона.

## Инструкция по запуску проекта локально

1. Клонировать репозиторий.
    - клонировать с SSH
    ```bash
    git clone git@gitlab.com:python_projects9153019/salary_info_api.git
    ```
    - клонировать с HTTPS
    ```bash
    git clone https://gitlab.com/python_projects9153019/salary_info_api.git
    ```
   
2. Cоздать и активировать виртуальное окружение, установить зависимости.

    - установить poetry
    - настроить и создать виртуальное окружение в папке проекта, установить зависимости, активировать виртуальное окружение   
    ```bash
    cd Seversta-FastApi
    poetry config virtualenvs.in-project true
    poetry install
    ```
   
3. В корневой директории cоздать .env файл по следующему шаблону:

    ```
   DB_HOST=''
   DB_PORT=''
   DB_NAME=''
   DB_USER=''
   DB_PASS=''
    ```
   
4. Применить миграции
    ```bash
    alembic upgrade head
    ```
   
5. Запустить проект
    ```bash
    uvicorn severstal_fastapi.main:app --reload
    ```

## Взаимодейтсвие с проектом

Взаимодействовать с сервисом можно через

- Swagger, в котором задокументированы возможности API и примеры запросов, перейдя по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Postman - сервис для создания, тестирования, документирования, публикации и обслуживания API