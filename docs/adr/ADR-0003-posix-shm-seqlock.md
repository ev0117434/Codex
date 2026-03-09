# ADR-0003: POSIX SHM + seqlock for quote transport

- Status: Accepted
- Date: 2026-03-09

## Context
Нужен быстрый обмен последними котировками между процессами с минимальной задержкой.

## Decision
Использовать POSIX shared memory (`/csm_quotes_v1`) и seqlock-протокол для консистентного чтения/записи слотов.

## Rationale
- Низкая latency и overhead по сравнению с внешним брокером для single-host.
- Детерминированная модель «последнее состояние по ключу».
- Seqlock даёт простой и эффективный способ избежать torn reads.

## Consequences
- Плюсы: скорость, простота runtime-инфры, predictable performance.
- Минусы: сложнее переносимость между ОС/окружениями, нужен аккуратный lifecycle SHM.
