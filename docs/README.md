# Crypto Spread Monitor — Architecture Documentation Hub

Этот раздел содержит полный комплект документации по архитектурным решениям для v1.1.

## Цель
Сделать **простую, лёгкую в сопровождении**, но при этом **надёжно работающую** систему мониторинга спреда между spot и futures рынками Binance и Bybit.

## Принципы выбора решений
1. **Simplicity first** — минимально достаточная сложность.
2. **Production-ready baseline** — стабильность и наблюдаемость с первого релиза.
3. **Incremental scalability** — возможность расширять без переписывания ядра.
4. **Fail-safe behavior** — при проблемах система деградирует контролируемо.
5. **Deterministic data flow** — предсказуемый пайплайн и прозрачные точки ответственности.

## Карта документов
- [1) Architecture Overview](./ARCHITECTURE_OVERVIEW.md) — итоговая целевая архитектура v1.1.
- [2) Principles & NFR](./PRINCIPLES_AND_NFR.md) — ключевые требования и ограничения.
- [3) Module Contracts](./MODULE_CONTRACTS.md) — контракты между компонентами.
- [4) Data Model & Formats](./DATA_MODEL_AND_FORMATS.md) — форматы данных и соглашения.
- [5) Operations Runbook](./OPERATIONS_RUNBOOK.md) — эксплуатация, восстановление, диагностика.
- [6) Testing Strategy](./TESTING_STRATEGY.md) — стратегия проверок для v1.1.
- [7) Roadmap v1.2+](./ROADMAP_V1_2_PLUS.md) — что расширяем после стабильного релиза.
- [8) Glossary & Style](./GLOSSARY_AND_STYLE.md) — словарь терминов и соглашения по стилю.
- [9) Assumptions & Limits](./ASSUMPTIONS_AND_LIMITS.md) — допущения и ограничения v1.1.
- [10) TODO Plan](./TODO_PLAN.md) — практический чек-лист задач v1.1.
- [11) Missing Information](./MISSING_INFORMATION.md) — актуальный реестр закрытых и открытых решений по требованиям.
- [12) Missing Information Questionnaire](./MISSING_INFORMATION_QUESTIONNAIRE.md) — заполненный вопросник с ответами заказчика и оставшимися пробелами.

## ADR (Architecture Decision Records)
- [ADR-0001: Python as implementation language](./adr/ADR-0001-python-runtime.md)
- [ADR-0002: Process-separated pipeline](./adr/ADR-0002-process-separated-pipeline.md)
- [ADR-0003: POSIX SHM + seqlock for quote transport](./adr/ADR-0003-posix-shm-seqlock.md)
- [ADR-0004: Unified Quote schema](./adr/ADR-0004-unified-quote-schema.md)
- [ADR-0005: Snapshot as primary output artifact](./adr/ADR-0005-snapshot-output.md)
- [ADR-0006: Observability baseline for v1.1](./adr/ADR-0006-observability-baseline.md)
- [ADR-0007: Simple deployment model for v1.1](./adr/ADR-0007-deployment-model.md)

## Status
- Все ADR имеют статус **Accepted** для версии v1.1.
- Документы ориентированы на быстрый запуск в production-lite режиме.
