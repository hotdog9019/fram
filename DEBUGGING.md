# Демонстрация отладки в VS Code

## Что показать преподавателю

Откройте файл `main.py` и поставьте breakpoints на строках:

- `total_score = calculate_total_score(`
- `average_score = calculate_average_score(scores)`
- `jury_decision = get_jury_decision(`

Дополнительно можно поставить breakpoint в `hackflow/submissions.py` на строке:

- `return calculate_total_score(scores) / len(scores)`

После этого откройте раздел Run and Debug в VS Code и запустите конфигурацию `Python: HackFlow`.

## Что смотреть в отладчике

Во время остановки программы покажите блок Variables и значения:

- `idea_score`: `8.5`;
- `prototype_score`: `9.0`;
- `presentation_score`: `7.5`;
- `total_score`: `25.0`;
- `average_score`: `8.333333333333334`;
- `passing_score`: `22`;
- `jury_decision`: `Проект проходит в финал, итоговый балл: 25.0`.

## Как показать поиск ошибки

1. Временно измените строку `return calculate_total_score(scores) / len(scores)` на `return calculate_total_score(scores) / 4`.
2. Запустите отладку заново.
3. На строке `average_score = calculate_average_score(scores)` нажмите Step Into.
4. Покажите, что `total_score` равен `25.0`, но `average_score` получается `6.25`.
5. Объясните, что ошибка в неверном делителе.
6. Верните строку к правильному виду: `return calculate_total_score(scores) / len(scores)`.

## Команды для проверки

```powershell
python main.py
python -m pytest
python -m flake8
git status
git log --oneline
```
