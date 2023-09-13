## API по взаимодействию с сервисом бронирования отелей

---
### Установка:
```
    git clone https://github.com/Arty3m/Booking.git
```
Далее необходимо перейти в директорию **Booking**

---

### Создание виртуального окружения
```
    python -m venv venv
```
---

### Активация виртуального окружения
```
    venv/Scripts/activate - Wndows
    . ./venv/Scripts/activate - Linux
```
---

### Установка зависимостей:
```
    pip install -r requirements.txt
```
---

### Запуск приложения:
```
    uvicorn app.main:app --reload
```
Ее необходимо запускать в командной строке, находясь в корневой директории проекта.

---
### Миграция данных в БД:
```
    alembic upgrade head
```