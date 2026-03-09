# ADR-0001: Python as implementation language

- Status: Accepted
- Date: 2026-03-09

## Context
Нужен быстрый time-to-market и простая поддержка v1.1.

## Decision
Использовать Python как основной runtime для всех модулей.

## Rationale
- Быстрая разработка и итерации.
- Богатая экосистема для REST/WS/IO.
- Низкий порог поддержки командой.

## Consequences
- Плюсы: скорость, гибкость, читаемость.
- Минусы: не максимальная raw-performance, требуется дисциплина в профилировании.
