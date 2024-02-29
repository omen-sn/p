# Вибір базового образу
FROM python:3.12-slim

# Встановлення робочої директорії у контейнері
WORKDIR /usr/src/app

# Встановлення Pipenv
RUN pip install pipenv

# Копіювання Pipfile та Pipfile.lock у контейнер
COPY Pipfile Pipfile.lock ./

# Встановлення залежностей з використанням Pipenv
# --system використовується для встановлення залежностей на рівні системи, а не в віртуальне середовище
# --deploy використовується для забезпечення відповідності Pipfile.lock
RUN pipenv install --system --deploy

# Копіювання всіх файлів проекту до контейнера
COPY . .

# Вказівка порту, який буде відкритий у контейнері
EXPOSE 8000

# Команда для запуску Django-сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
