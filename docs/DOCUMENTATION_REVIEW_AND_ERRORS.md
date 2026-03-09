# Ревью документации: замечания, ошибки и противоречия

Дата ревью: 2026-03-09.

## Статус выполнения

Все ранее обозначенные пункты **P0 / P1 / P2 выполнены** и отражены в актуальных документах:
- `DATA_MODEL_AND_FORMATS.md`
- `OPERATIONS_RUNBOOK.md`
- `PRINCIPLES_AND_NFR.md`
- `MODULE_CONTRACTS.md`
- `README.md`
- `GLOSSARY_AND_STYLE.md`
- `ASSUMPTIONS_AND_LIMITS.md`
- `adr/ADR-0006-observability-baseline.md`

## Что было исправлено

### P0
1. Исправлен пример расчёта `SPREAD%` на корректное значение (`0.1536`).
2. Исправлен startup order: `shm_init` перенесён до запуска writer-процессов.

### P1
1. Зафиксирован формат имени snapshot: `spread_snapshot_YYYYMMDDTHHMMSSZ.txt`.
2. Уточнены timestamp единицы: во всех контрактах `int64` в `ns`.
3. Добавлен отдельный словарь терминов и соглашения по стилю.

### P2
1. Добавлен документ `Assumptions and Limits`.
2. Добавлен валидный пример snapshot с проверяемой формулой.
3. Добавлена таблица `Компонент → SLO → Метрика → Alert-порог` в runbook.

## Примечание

Этот файл сохранён как исторический журнал ревью и выполненных корректировок.
