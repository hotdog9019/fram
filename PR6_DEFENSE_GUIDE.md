# Шпаргалка для сдачи ПР6

## Что сдавать

1. Ссылка на GitHub:
   `https://github.com/hotdog9019/fram`
2. Коммит с меткой `PR6:`.
3. Файл отчета: `REPORT_PR6.md`.
4. Обновленный `README.md`.
5. Демонстрация работающего Django-проекта.

## Команды перед защитой

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python -m pytest
python -m flake8
python manage.py runserver
```

Проверка static-файлов:

```powershell
python manage.py findstatic homepage/css/style.css homepage/img/logo.svg homepage/js/main.js
```

## Что открыть в браузере

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/teams/
http://127.0.0.1:8000/teams/1/
http://127.0.0.1:8000/submissions/
http://127.0.0.1:8000/submissions/1/
http://127.0.0.1:8000/nonexistent/
```

## Что показать в коде

1. Базовый шаблон:
   `templates/base.html`

   Здесь есть `{% load static %}`, подключение Bootstrap, свой CSS, навигация,
   блоки `{% block title %}` и `{% block content %}`.

2. Наследование шаблонов:
   `teams/templates/teams/team_list.html`

   Показать строку:

   ```django
   {% extends "base.html" %}
   ```

3. Include-фрагменты:
   `templates/includes/navigation.html`
   `teams/templates/teams/includes/team_card.html`
   `submissions/templates/submissions/includes/submission_status.html`

4. Контекст из view:
   `teams/views.py`

   View загружает данные, формирует словарь `context` и вызывает:

   ```python
   return render(request, "teams/team_list.html", context)
   ```

5. Циклы и условия:
   `teams/templates/teams/team_list.html`
   `submissions/templates/submissions/submission_detail.html`

   Там используются `{% for %}`, `{% empty %}`, `{% if %}`.

6. Именованные URL:
   `templates/includes/navigation.html`

   Пример:

   ```django
   {% url 'teams:teams' %}
   ```

7. Static-файлы:
   `homepage/static/homepage/css/style.css`
   `homepage/static/homepage/img/logo.svg`
   `homepage/static/homepage/js/main.js`

## Короткий рассказ преподавателю

В ПР5 HTML формировался прямо во view-функциях строками. В ПР6 я перенес
разметку в Django-шаблоны. Теперь view-функции отвечают за загрузку данных из
JSON, поиск объектов и подготовку контекста, а шаблоны отвечают за отображение.

В проекте есть общий `base.html`, от которого наследуются страницы. Навигация и
подвал вынесены в include-шаблоны. Карточки команд и проектов тоже вынесены в
отдельные include-фрагменты. Ссылки формируются через `{% url %}`, а CSS, JS и
логотип подключаются через `{% static %}`.

## Частые вопросы и ответы

### Зачем нужен `base.html`?

Чтобы не повторять одинаковую HTML-структуру на каждой странице. В нем лежат
`html`, `head`, подключение CSS, навигация и общие блоки.

### Что делает `{% extends "base.html" %}`?

Он связывает дочерний шаблон с базовым. Дочерняя страница заполняет блоки,
которые объявлены в `base.html`.

### Что такое контекст шаблона?

Это словарь данных, который view-функция передает в шаблон. Например,
`teams/views.py` передает список команд под именем `teams`.

### Где используются циклы?

В списках команд и проектов. Например, `team_list.html` перебирает команды:

```django
{% for team in teams %}
```

### Где используются условия?

В шаблонах статусов. Например, если команда зарегистрирована, показывается
зеленый badge, иначе серый.

### Какие фильтры используются?

`length` считает количество элементов, `default` подставляет значение по
умолчанию, `floatformat` форматирует число, `date` форматирует дату.

### Зачем нужен `{% url %}`?

Чтобы не писать адреса вручную. Если маршрут изменится, ссылка продолжит
работать через имя маршрута.

### Зачем нужен `{% static %}`?

Чтобы Django правильно находил CSS, изображения и JavaScript в static-каталогах
приложений.

### Почему бизнес-логика не в шаблонах?

Шаблон отвечает только за отображение. Загрузка JSON, поиск объектов и расчеты
остаются во view-функциях и модулях предметной области.

## Мини-чеклист перед отправкой

- `python manage.py check` проходит.
- `python -m pytest` проходит.
- `python -m flake8` проходит.
- Главная страница открывается.
- Страница команд открывается.
- Страница проектов открывается.
- 404 открывается на `/nonexistent/`.
- В Git есть коммит `PR6: ...`.
