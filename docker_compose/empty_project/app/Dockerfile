# Укажите необходимую версию python
FROM python:3.10

# Выберите папку, в которой будут размещаться файлы проекта внутри контейнера
WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE=example.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

# Установите зависимости
RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY .. .


EXPOSE 8000
