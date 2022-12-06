# Простой чат на django + aiohttp + websockets

Проект в контейнерах, чтобы собрать;
```
docker-compose up -d
```

Накатить миграции на БД;
```
docker-compose run --rm --entrypoint python app manage.py migrate
```

Создать суперпользователя для доступа к админке `/admin/`:
```
docker-compose run --rm --entrypoint python app manage.py createsuperuser
```

Доступны точки вызова API:
```
/api/v1/chats
/api/v1/chats/[pk]
```
Вебсокеты для соединения;
```
/api/v1/ws
```

