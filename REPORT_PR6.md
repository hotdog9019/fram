# Отчет по практической работе 6

## 1. Общие сведения

Практическая работа: № 6. Django-шаблоны

ФИО студента: Элизбарян Артем Гайкович

Группа: ЭФБО-14-24

Индивидуальный проект: HackFlow

## 2. Цель работы

Изучить систему шаблонов Django и применить ее в индивидуальном проекте:
перенести HTML из Python-кода view-функций в шаблоны, использовать контекст,
наследование, включаемые шаблоны, фильтры, именованные URL и static-файлы.

## 3. Выполненные материалы Яндекс Практикума

| Раздел | Выполненные темы |
| --- | --- |
| Раздел 04. Основы веб-разработки | HTML в Django: шаблоны веб-страниц |
| Раздел 04. Основы веб-разработки | HTML-шаблоны из частей: include, extends, block |
| Раздел 04. Основы веб-разработки | Словарь контекста, ветвление и циклы |
| Раздел 04. Основы веб-разработки | Ссылки в шаблонах: name и namespace |
| Раздел 04. Основы веб-разработки | Фильтры шаблонов |
| Раздел 04. Основы веб-разработки | Подключение стилей, картинок и скриптов |

## 4. Доработка индивидуального проекта

В проекте создана структура шаблонов:

- `templates/base.html` - базовый шаблон сайта;
- `templates/includes/navigation.html` - общая навигация;
- `templates/includes/footer.html` - общий подвал;
- `homepage/templates/homepage/index.html` - главная страница;
- `homepage/templates/homepage/404.html` - страница ошибки 404;
- `teams/templates/teams/team_list.html` - список команд;
- `teams/templates/teams/team_detail.html` - страница команды;
- `submissions/templates/submissions/submission_list.html` - список проектов;
- `submissions/templates/submissions/submission_detail.html` - страница проекта.

Повторяющиеся элементы вынесены в include-шаблоны:

- `teams/templates/teams/includes/team_card.html`;
- `submissions/templates/submissions/includes/submission_card.html`;
- `submissions/templates/submissions/includes/submission_status.html`.

View-функции больше не формируют HTML-строки. Они загружают данные из JSON,
создают объекты предметной области, подготавливают контекст и вызывают
`render()`.

В шаблонах используются:

- наследование через `{% extends "base.html" %}`;
- блоки `{% block title %}` и `{% block content %}`;
- включение фрагментов через `{% include %}`;
- циклы `{% for %}` и `{% empty %}`;
- условия `{% if %}`;
- фильтры `length`, `default`, `floatformat`, `date`;
- именованные URL через `{% url %}`;
- static-файлы через `{% load static %}` и `{% static %}`.

Для оформления добавлены static-файлы:

- `homepage/static/homepage/css/style.css`;
- `homepage/static/homepage/img/logo.svg`;
- `homepage/static/homepage/js/main.js`.

Git-репозиторий: https://github.com/hotdog9019/fram

## 5. Проверка

Проект проверен командами:

```powershell
python manage.py check
python manage.py findstatic homepage/css/style.css homepage/img/logo.svg homepage/js/main.js
python -m pytest
python -m flake8
```

## 6. Git

Для фиксации результата создан коммит с префиксом `PR6:`.

## 7. Вывод

В ходе ПР6 веб-интерфейс HackFlow был переведен с формирования HTML в
Python-коде на систему шаблонов Django. Представления теперь отвечают за
подготовку данных и контекста, а отображение вынесено в шаблоны. В проекте
используются базовый шаблон, наследование, include-фрагменты, условия, циклы,
фильтры, именованные маршруты и static-файлы.
