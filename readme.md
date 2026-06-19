# TeamFinder — вариант 3

Веб-приложение для поиска команды и проектов. Реализован **вариант 3**: навыки проектов и фильтрация по навыкам на главной странице.

Стек: **Django 5.2**, **PostgreSQL**, **Docker Compose** (БД), HTML/CSS/JS из стартового набора Практикума.

---

## Инструкция для ревьюера

### Требования

- Python 3.10+
- Docker и Docker Compose (для PostgreSQL)
- Git не обязателен

### Запуск на Windows (PowerShell)

```powershell
cd team-finder-practicum-v3
copy .env_example .env
docker compose up -d
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial.json
python manage.py runserver
```

Открыть: **http://127.0.0.1:8000** — редирект на `/project/list/`.

### Запуск на Linux / macOS

```bash
cd team-finder-practicum-v3
cp .env_example .env
docker compose up -d
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial.json
python manage.py runserver
```

### Остановка PostgreSQL

```bash
docker compose down
```

Данные БД сохраняются в Docker volume `postgres_data`.

---

## Тестовые аккаунты

| Email | Пароль | Описание |
|-------|--------|----------|
| anna@example.com | testpass123 | 2 проекта, навыки Python/Django |
| boris@example.com | testpass123 | 1 проект, участник проекта Анны |
| vika@example.com | testpass123 | 1 закрытый проект |
| admin@example.com | adminpass123 | администратор, `/admin/` |

У каждого пользователя минимум один проект. Файл фикстур: `fixtures/initial.json`.

---

## Что проверить (вариант 3)

| Страница | URL | Действие |
|----------|-----|----------|
| Главная | `/project/list/` | карточки проектов, фильтр по навыкам (`?skill=Python`) |
| Регистрация | `/users/register/` | после submit → `/users/login/` |
| Вход | `/users/login/` | после входа → `/projects/list` |
| Профиль | `/users/1/` | ФИО, контакты, проекты пользователя |
| Редактирование | `/users/edit-profile/` | только для своего аккаунта |
| Смена пароля | `/users/change-password/` | только авторизованным |
| Список пользователей | `/users/list/` | карточки, пагинация 12 |
| Проект | `/projects/1/` | навыки (AJAX), участие, завершение |
| Создание проекта | `/projects/create-project/` | только авторизованным |
| Админка | `/admin/` | admin@example.com |

**Навыки (AJAX):** войти как anna@example.com → свой проект → «+ Добавить навык» → autocomplete / создать новый → удалить через ×.

**Выход:** меню пользователя → «Выйти» → главная без 404.

---

## Структура проекта

```
team-finder-practicum-v3/
├── team_finder/          # настройки Django
├── users/                # User, auth, профиль
├── projects/             # Project, Skill, CRUD, фильтры
├── templates_var3/       # HTML-шаблоны (вариант 3)
├── static/               # CSS, JS, изображения
├── fixtures/             # тестовые данные
├── media/                # аватары пользователей
├── docs/                 # материалы Практикума
├── docker-compose.yml    # PostgreSQL
├── requirements.txt
├── .env_example
└── manage.py
```

---

## Переменные окружения (.env)

| Переменная | Значение |
|------------|----------|
| DJANGO_SECRET_KEY | секретный ключ Django |
| DJANGO_DEBUG | True |
| POSTGRES_DB | team_finder |
| POSTGRES_USER | team_finder |
| POSTGRES_PASSWORD | team_finder |
| POSTGRES_HOST | localhost |
| POSTGRES_PORT | 5432 |
| TASK_VERSION | **3** (обязательно) |

---

## Реализованный функционал

- Регистрация, вход, выход, профиль, редактирование, смена пароля
- Список и создание/редактирование проектов
- Участие в проектах, завершение проекта автором
- **Вариант 3:** навыки проекта (add/remove/autocomplete), фильтр на главной
- Пагинация: 12 проектов и 12 пользователей на страницу
- PostgreSQL + Docker Compose + volume для данных
- Django Admin

---

## Отклонения от текста урока

| Тема | Решение |
|------|---------|
| После регистрации | redirect на `/users/login/` (чек-лист ревью) |
| `skills.js` | адаптирован под JSON `{skill_id, created, added}` |
| Шаблоны | исправлен merge conflict, pagination, кнопка «Создать проект» |
| `select_related` в `user_list_view` | не используется: в варианте 3 шаблон списка пользователей читает только поля модели `User` (`name`, `surname`, `about`, `avatar`), без обращений к ForeignKey |

---

## Возможные проблемы

**Docker не запускается:** убедитесь, что Docker Desktop запущен. Порт 5432 не занят другим PostgreSQL.

**Ошибка подключения к БД:** проверьте `.env` — параметры должны совпадать с `docker-compose.yml`.

**Аватары не отображаются после loaddata:** в архиве включена папка `media/avatars/`. Если файлов нет — зарегистрируйте нового пользователя (avatar генерируется автоматически).

**Порт 8000 занят:** `python manage.py runserver 8001`

---

## Первоначальная настройка (из стартового набора)

Подробности по переменным и Docker — в разделе «Инструкция для ревьюера» выше.

Пример `.env`:

```bash
copy .env_example .env   # Windows
cp .env_example .env     # Linux/macOS
```

Обязательно указать `TASK_VERSION=3` — используются шаблоны из `templates_var3/`.
