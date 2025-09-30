# 🌍 OpenWorld — Энциклопедия статей

> *Создавайте, редактируйте и просматривайте статьи в удобной веб-энциклопедии.*

OpenWorld — это простая, но гибкая энциклопедия на Django, позволяющая пользователям добавлять и редактировать статьи. Проект развертывается через Docker, что упрощает установку и запуск на любом устройстве.

---

## 🚀 Быстрый старт

### 1. Установите Docker и Docker Compose

Убедитесь, что у вас установлены:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

> 💡 На Linux/Mac: `docker-compose` часто входит в пакет `docker`.  
> На Windows: установите [Docker Desktop](https://www.docker.com/products/docker-desktop).

---

### 2. Клонируйте репозиторий

```bash
git clone https://github.com/ваш-репозиторий/OpenWorld.git
cd OpenWorld
```

3. Запустите проект через Docker
```bash
docker-compose up --build
```

4. Сделать миграции

```bash
docker-compose exec web python manage.py migrate
```

# Проект автоматически:

Создаст базу данных (по умолчанию Postgres)
- Применит миграции
- Запустит сервер Django на http://localhost:8000