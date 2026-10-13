# Отчет по практической работе 6

## 1. Общие сведения

Практическая работа: № 6. Django-шаблоны

ФИО студента: Элизбарян Артем Гайкович

Группа: ЭФБО-14-24

Индивидуальный проект: HackFlow

## 2. Цель работы

Изучить систему шаблонов Django и применить ее в индивидуальном проекте:
перенести HTML из Python-кода view-функций в шаблоны, использовать контекст,
наследование, include-фрагменты, фильтры, именованные URL и static-файлы.

## 3. Доработка индивидуального проекта

В проекте создан базовый шаблон `templates/base.html`, общая навигация
`templates/includes/navigation.html` и общий подвал
`templates/includes/footer.html`. Страницы приложений `homepage`, `teams` и
`submissions` перенесены в шаблоны приложений.

Реализованы:

- наследование шаблонов через `{% extends %}`;
- блоки `{% block title %}` и `{% block content %}`;
- включаемые шаблоны через `{% include %}`;
- передача данных из view-функций через контекст;
- условия `{% if %}` и циклы `{% for %}`;
- фильтры `length`, `default`, `floatformat`, `date`;
- именованные URL через `{% url %}`;
- static-файлы через `{% load static %}` и `{% static %}`.

Добавлены static-файлы:

- `homepage/static/homepage/css/style.css`;
- `homepage/static/homepage/img/logo.svg`;
- `homepage/static/homepage/js/main.js`.

Git-репозиторий: https://github.com/hotdog9019/fram

## 4. Результат работы

Веб-интерфейс HackFlow переведен с формирования HTML-строк в Python на
шаблонную архитектуру Django. View-функции теперь загружают данные из JSON,
используют объектную модель ПР3, формируют контекст и вызывают `render()`.
Отображение данных выполняется в шаблонах.

## 5. Проверка

Проект проверен командами:

```powershell
python manage.py check
python manage.py findstatic homepage/css/style.css homepage/img/logo.svg homepage/js/main.js
python -m pytest
python -m flake8
```

## 6. Вывод

В ходе ПР6 проект HackFlow получил полноценный шаблонный уровень Django.
Базовый шаблон, дочерние шаблоны, include-фрагменты, контекст, условия, циклы,
фильтры, именованные маршруты и static-файлы подготовили проект к дальнейшему
развитию веб-интерфейса.
