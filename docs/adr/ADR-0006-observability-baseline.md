# ADR-0006: Observability baseline for v1.1

- Status: Accepted
- Date: 2026-03-09

## Context
Система зависит от сети и многокомпонентна; без наблюдаемости поиск причин деградации слишком дорог.

## Decision
Обязательный baseline: структурированные логи + базовые метрики + health checks.

## Rationale
- Быстрая диагностика stale spikes, reconnect storm, write/read lag.
- Упрощение эксплуатации в single-host режиме.

## Consequences
- Плюсы: предсказуемая операционная модель.
- Минусы: небольшой overhead на логирование и метрики.
