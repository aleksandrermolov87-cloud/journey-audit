# Семейство: имитация когнитивной нагрузки

> Русская версия `SKILL.md`. Справочники — `references/ru/`.

Вопрос семейства: **на каких шагах путь требует от человека больше внимания, памяти и решений, чем нужно для задачи, и что из этого можно забрать.** Логику карты и краевые сценарии не оценивай; если заметил, запиши строкой в отчёт → «Передать другим семействам».

Всё здесь — модель, а не измерение. В отчёте показывай формулу и вклады, а не только итог.

## Вход

`journey.json`, `frame.md`, исходник, снимки и тексты интерфейса, если есть.

## Методы

| # | Метод | Файл | Что даёт |
|---|---|---|---|
| 1 | Уточнение признаков `load` по шагам | `references/ru/cognitive-load.md` → «Что заполнять» | Честные значения решений, вариантов, памяти, терминов, ожидания |
| 2 | Индекс, KLM, усталость, точки ухода | `references/ru/cognitive-load.md` + скрипт | Таблица по шагам |
| 3 | Чувствительность к персоне | `references/ru/persona-sensitivity.md` | Шаги, которые ломаются только для части людей |
| 4 | Эвристики по шагам | `references/ru/heuristics.md` | Какие принципы нарушены там, где индекс высокий, и почему |
| 5 | Внутренняя и лишняя нагрузка, рычаги | `references/ru/cognitive-load.md` → «Внутренняя и лишняя» | Что резать, что оставить, что показать яснее |

### Уточнение признаков

Значения `load` в `journey.json` выставил оркестратор при нормализации, они грубые. `journey.json` не меняй: скопируй его в `<work>/load/journey.load.json`, уточни `load` там и запиши каждое изменение в `<work>/load/load-overrides.json`:

```json
[{"step": "s7", "field": "context_switches", "from": 0, "to": 1, "why": "адрес копируют из мессенджера"}]
```

### Расчёт

```bash
J=<work>/load/journey.load.json
python3 <Script> load $J --lang ru --persona-tech mid  --persona-patience mid  --json > <work>/load/load-mid.json
python3 <Script> load $J --lang ru --persona-tech low  --persona-patience low  --json > <work>/load/load-low.json
python3 <Script> load $J --lang ru --persona-tech high --persona-patience high --json > <work>/load/load-high.json
python3 <Script> curve $J --lang ru --persona-tech low --persona-patience low -o <work>/load/load-curve.svg
```

`<Script>` — `journey-audit/scripts/journey_check.py`, путь передаёт оркестратор.

**Ветки**: скрипт считает основной путь. Для ветки собери временный JSON (ветка как `steps`) и прогони `load` на нём; результат — `load/load-branches.json`.

**Неизвестное ожидание** (`wait_s: "unknown"`) скрипт считает нулём. Если в доказательствах есть замеры, посчитай сценарий с ними отдельно (`load-wait-scenario.json`) и укажи источник.

## Выход

- `<work>/load/findings.json` — по контракту `journey-audit/references/ru/findings-contract.md`, id `LOAD-NN`, отчёт — в `report_md`. Код проверки: `C-<шаг>` для индекса и усталости, `H<n>` / `K<n>` для эвристики, `KLM` для времени. В `detail` — индекс, уровень, главные вклады и профиль персоны. Трение, которое защищает пользователя, помечай `useful_friction: true`.
- `journey.load.json`, `load-overrides.json`, `load-*.json`, `load-curve.svg`.

## Границы

Не выдавай индекс за прогноз конверсии. Тяжесть: перегрузка (≥ 70) или точка ухода на главном пути — `high`; `critical` — только если перегрузка ведёт к неверному решению или вреду (подтвердил не читая неверные данные, не заметил предупреждение) — как в определении контракта. Остальное — `medium`. Если перегрузка появилась только после твоих уточнений, укажи индекс до и после.
