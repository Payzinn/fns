# Приложение по заполнению документа для ФНС

## Запуск

### Через докер

### 1. Вводим команду и всё запустится
```cmd
docker-compose up --build --force-recreate
```

### Через python

### 1. Создание виртуального окружения
```cmd
python -m venv venv
```
### или
```cmd
python3 -m venv venv
```
### 2. Вход в виртуальное окружение
```cmd
venv\Scripts\activate
```
### 3. Устанавливаем зависимости
```cmd
pip install -r requirements.txt
```
### 4. Запуск
```cmd
python manage.py runserver
```
