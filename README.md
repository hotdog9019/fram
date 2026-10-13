# HackFlow

HackFlow - учебный проект для организации хакатона. В ПР3 проект был
переведен на объектную модель, а в ПР5 к нему добавлен базовый веб-интерфейс
на Django.

## Предметная область

Проект описывает проведение хакатона: регистрацию команд, хранение участников,
сдачу проектов, проверку дедлайна, расчет оценок жюри и определение финалистов.

## Технологии

- Python
- Django 5.2
- HTML
- Bootstrap 5.3
- JSON как временное хранилище данных
- pytest
- flake8

## Объектная модель ПР3

Основные классы:

- `Team` - команда, участники, статус регистрации и скидка.
- `Hackathon` - настройки хакатона, лимит команд, дедлайн и проходной балл.
- `Submission` - сдача проекта, связанная с объектом команды.

Классы поддерживают `from_data()` и `to_data()`, поэтому JSON-данные
преобразуются в объекты и обратно.

## Django-структура ПР5

```text
hackflow_site/
  settings.py
  urls.py
  asgi.py
  wsgi.py
homepage/
  urls.py
  views.py
teams/
  urls.py
  views.py
submissions/
  urls.py
  views.py
hackflow/
  statistics.py
  storage.py
  submissions.py
  teams.py
  utils.py
data/
  hackathon.json
  teams.json
  submissions.json
tests/
manage.py
main.py
```

## Django-приложения

- `homepage` - главная страница, общий HTML-каркас `page()` и обработчик 404.
- `teams` - список команд и страница отдельной команды.
- `submissions` - список сданных проектов и страница отдельной сдачи.

Приложения зарегистрированы в `INSTALLED_APPS`, а маршруты подключены через
`include()` в `hackflow_site/urls.py`.

## Реализованные страницы

| URL | View-функция | Назначение |
| --- | --- | --- |
| `/` | `homepage.views.index` | Главная страница и статистика хакатона |
| `/teams/` | `teams.views.teams` | Список команд |
| `/teams/<int:team_id>/` | `teams.views.team_detail` | Карточка команды |
| `/submissions/` | `submissions.views.submissions` | Список проектов |
| `/submissions/<int:team_id>/` | `submissions.views.submission_detail` | Карточка проекта команды |
| любой несуществующий адрес | `homepage.views.page_not_found` | Страница 404 |

## Данные

Веб-интерфейс использует данные из ПР3:

- `data/hackathon.json`
- `data/teams.json`
- `data/submissions.json`

Переход на Django ORM будет выполняться на следующих практических работах.
На текущем этапе JSON-хранилище сохранено специально, чтобы показать связь с
объектной моделью ПР3.

## Запуск консольной версии

```powershell
python main.py
```

## Запуск Django-приложения

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

После запуска открыть в браузере:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/teams/`
- `http://127.0.0.1:8000/submissions/`
- `http://127.0.0.1:8000/nonexistent/`

## Проверка

```powershell
python -m pytest
python -m flake8
python manage.py check
```

Текущее состояние проекта: консольная версия ПР3 сохранена, поверх нее добавлен
начальный веб-слой Django для ПР5.
