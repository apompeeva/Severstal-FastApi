from fastapi import FastAPI

from severstal_fastapi.endpoints import router

app = FastAPI()

app.include_router(router)

"""
ToDo:
- Преобразовать в формат Orm запрос для получения статистики
- Запрос рулонов по диапазону
- Обработка исключений
- Тестовое окружение
- Тесты 
- README
- Docker
"""