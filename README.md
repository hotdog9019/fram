# HackFlow

HackFlow - учебный проект для организации хакатона. В ПР3 проект был
переведен на объектную модель, в ПР5 получил базовый веб-интерфейс на Django,
а в ПР6 веб-часть переведена на Django-шаблоны и static-файлы.

## Предметная область

Проект описывает проведение хакатона: регистрацию команд, хранение участников,
сдачу проектов, проверку дедлайна, расчет оценок жюри и определение финалистов.

## Технологии

- Python
- Django 5.2
- Django Template Language
- HTML
- Bootstrap 5.3
- CSS и JavaScript через Django static files
- JSON как временное хранилище данных
- pytest
- flake8
- Git

## Объектная модель ПР3

Основные классы:

- `Team` - команда, участники, статус регистрации и скидка.
- `Hackathon` - настройки хакатона, лимит команд, дедлайн и проходной балл.
- `Submission` - сдача проекта, связанная с объектом команды.

Классы поддерживают `from_data()` и `to_data()`, поэтому JSON-данные
преобразуются в объекты и обратно.

## Django-структура

```text
hackflow_site/
  settings.py
  urls.py
homepage/
  templates/homepage/
  static/homepage/
  urls.py
  views.py
teams/
  templates/teams/
  urls.py
  views.py
submissions/
  templates/submissions/
  urls.py
  views.py
templates/
  base.html
  includes/
hackflow/
data/
tests/
manage.py
main.py
```

## Django-приложения

- `homepage` - главная страница, обработчик 404, CSS, JS и логотип.
- `teams` - список команд и страница отдельной команды.
- `submissions` - список сданных проектов и страница отдельной сдачи.

Приложения зарегистрированы в `INSTALLED_APPS`. Маршруты подключены через
`include()` в `hackflow_site/urls.py`.

## Шаблоны ПР6

Для формирования страниц используются Django-шаблоны. View-функции готовят
данные и передают их в шаблоны через контекст.

Общий базовый шаблон:

```text
templates/base.html
```

Дочерние шаблоны используют наследование:

```django
{% extends "base.html" %}
{% block content %}{% endblock %}
```

Повторяющиеся фрагменты вынесены в include-шаблоны:

- `templates/includes/navigation.html`
- `templates/includes/footer.html`
- `teams/templates/teams/includes/team_card.html`
- `submissions/templates/submissions/includes/submission_card.html`
- `submissions/templates/submissions/includes/submission_status.html`

В шаблонах используются:

- `{% for %}` и `{% empty %}` для вывода списков;
- `{% if %}` для статусов и отсутствующих объектов;
- фильтры `length`, `default`, `floatformat`, `date`;
- `{% url %}` для именованных маршрутов;
- `{% load static %}` и `{% static %}` для CSS, JS и логотипа.

## Реализованные страницы

| URL | View-функция | Шаблон |
| --- | --- | --- |
| `/` | `homepage.views.index` | `homepage/index.html` |
| `/teams/` | `teams.views.teams` | `teams/team_list.html` |
| `/teams/<int:team_id>/` | `teams.views.team_detail` | `teams/team_detail.html` |
| `/submissions/` | `submissions.views.submissions` | `submissions/submission_list.html` |
| `/submissions/<int:team_id>/` | `submissions.views.submission_detail` | `submissions/submission_detail.html` |
| неизвестный адрес | `homepage.views.page_not_found` | `homepage/404.html` |

## Данные

Веб-интерфейс использует данные из ПР3:

- `data/hackathon.json`
- `data/teams.json`
- `data/submissions.json`

Переход на Django ORM будет выполняться на следующих практических работах.

## Запуск

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

После запуска открыть:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/teams/`
- `http://127.0.0.1:8000/submissions/`

## Проверка

```powershell
python -m pytest
python -m flake8
python manage.py check
python manage.py findstatic homepage/css/style.css homepage/img/logo.svg homepage/js/main.js
```

Текущее состояние проекта: консольная версия ПР3 сохранена, Django-интерфейс
работает через шаблоны, контекст, include-фрагменты и static-файлы.
