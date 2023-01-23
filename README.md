## Initial project setup

### Нужно установить зависимости и в файле .env необходимо указать урл для подключения к бд

```shell
poetry install
cp ./base/.env.example ./base/.env
```

### Нужно установить миграции и фикстуры
```shell
python manage.py migrate
python manage.py loaddata fixtures/User.json 
python manage.py loaddata fixtures/Note.json 
python manage.py loaddata fixtures/Ad.json 
python manage.py loaddata fixtures/Achievement.json 
```

### Чтобы запустить проект
```shell
python manage.py runserver
```

### Чтобы запустить тесты
```shell
python manage.py test
```

### В репозитории лежил файл дял импорта реквеста в postman "Django.postman_collection.json"

