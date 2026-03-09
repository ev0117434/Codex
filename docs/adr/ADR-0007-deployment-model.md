# ADR-0007: Simple deployment model for v1.1

- Status: Accepted
- Date: 2026-03-09

## Context
Цель — быстрый ввод в эксплуатацию без сложного orchestration stack.

## Decision
Single-host deployment с process supervisor и файловыми артефактами (logs/snapshots).

## Rationale
- Минимум инфраструктурных зависимостей.
- Быстрый recovery и простая отладка.
- Достаточно для подтверждения ценности v1.1.

## Consequences
- Плюсы: быстрый запуск, низкая стоимость сопровождения.
- Минусы: ограниченная отказоустойчивость, горизонтальное масштабирование позже.
