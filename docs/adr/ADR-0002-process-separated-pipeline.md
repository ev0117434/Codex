# ADR-0002: Process-separated pipeline

- Status: Accepted
- Date: 2026-03-09

## Context
Нужно разделить ответственность и упростить диагностику по стадиям пайплайна.

## Decision
Строим систему как набор независимых процессов: discovery, collectors, normalizer, spread_reader.

## Rationale
- Локализация отказов по процессам.
- Упрощённые контракты между модулями.
- Независимое масштабирование в будущем.

## Consequences
- Плюсы: supportability, прозрачность, контролируемая деградация.
- Минусы: межпроцессная координация и lifecycle management.
