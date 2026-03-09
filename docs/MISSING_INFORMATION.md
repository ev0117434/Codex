# Реестр решений и недостающей информации (v1.1)

Документ синхронизирован с текущими решениями v1.1: критические пункты Day-1 закрыты и зафиксированы как `answered`.

## Статусы
- `answered` — решение зафиксировано.
- `pending` — требуется уточнение.
- `delegated` — решение делегировано исполнителю, нужно предложить и утвердить.

Источник уже зафиксированных решений: ответы пользователя в `docs/MISSING_INFORMATION_QUESTIONNAIRE.md`.

---

## 1) Бизнес-правила и продукт

| ID | Статус | Решение |
|---|---|---|
| BR-01 | answered | Для v1.1 используем только `spot vs perpetual` (без quarterly). |
| BR-02 | answered | Исключений по символам нет. |
| BR-03 | answered | Фильтр ликвидности не применяется. |
| BR-04 | answered | Публикуется только положительный spread-сигнал (рабочее правило: spot дешевле futures). |
| BR-05 | answered | Выдача только в файл snapshot (без API/stream). |

## 2) SLA/SLO

| ID | Статус | Решение |
|---|---|---|
| SLO-01 | answered | Целевая end-to-end latency: p95 = 500ms, p99 = 500ms. |
| SLO-02 | answered | Допустимая доля stale: 50%. |
| SLO-03 | answered | Целевая доступность: 100%. |
| SLO-04 | answered | RTO/RPO не используются в v1.1. |

## 3) Технические параметры

| ID | Статус | Решение |
|---|---|---|
| TECH-01 | answered | `STALENESS_THRESHOLD = 60s`. |
| TECH-02 | answered | Не периодический режим: 1 сигнал по symbol+direction, затем cooldown 1 час. |
| TECH-03 | answered | `MAX_SLOTS = 4096`, `SLOT_SIZE = 256 bytes` (≈1 MiB payload + служебный запас), резерв роста x2 без смены API. |
| TECH-04 | answered | TTL snapshot-файлов отсутствует. |
| TECH-05 | answered | Формальная политика лог-ротации отсутствует. |

## 4) Источники данных и устойчивость

| ID | Статус | Решение |
|---|---|---|
| DATA-01 | answered | Binance Spot REST `https://api.binance.com`, WS `wss://stream.binance.com:9443/ws`; Binance USDⓈ-M Perp REST `https://fapi.binance.com`, WS `wss://fstream.binance.com/ws`; Bybit Spot/Linear REST `https://api.bybit.com` (v5), WS `wss://stream.bybit.com/v5/public/spot` и `wss://stream.bybit.com/v5/public/linear`. |
| DATA-02 | answered | Лимиты фиксируются по `X-MBX-USED-WEIGHT-*` (Binance) и `X-Bapi-Limit-*` (Bybit), WS: ≤300 connect attempts/5m/IP (Binance). Стратегия reconnect/backoff: 1s→2s→4s→8s→16s→30s (cap 30s) + jitter ±20%. При `429`: пауза по `Retry-After`/экспоненциальный backoff; при `ban/418`: охлаждение 5–15 мин + алерт в лог; при timeout/network: повтор с backoff, не более 10 подряд перед деградацией источника. |
| DATA-03 | answered | Фолбэк-источник не требуется. |
| DATA-04 | answered | Proxy/региональный routing не требуется. |

## 5) Контракты данных

| ID | Статус | Решение |
|---|---|---|
| SCHEMA-01 | answered | `Quote`: `exchange`, `market`, `symbol`, `best_bid`, `best_ask`, `ts_exchange`, `ts_receive`, `ts_normalized` (все timestamp в ns). |
| SCHEMA-02 | answered | Enum: `exchange in {binance, bybit}`, `market in {spot, futures}`. |
| SCHEMA-03 | answered | Истинное время для staleness: `ts_receive`. |
| SCHEMA-04 | answered | В snapshot вводится заголовок `# version: 1`; при отсутствии заголовка consumer трактует файл как `version: 1` (backward-compatible для v1.1). |

## 6) Эксплуатация

| ID | Статус | Решение |
|---|---|---|
| OPS-01 | answered | Запуск: bare metal VPS. |
| OPS-02 | answered | Baseline observability: structured logs (JSON/plain), counters `service_starts_total`, `quotes_received_total`, `reconnect_total`, `snapshot_write_total`, health-check CLI (`snapshot/healthcheck.py`), ежедневная проверка логов. |
| OPS-03 | answered | Алерты не требуются; только лог-файлы скриптов. |
| OPS-04 | answered | Минимальная on-call модель: best-effort support 10:00–19:00 UTC+3 (пн–пт), реакция на инцидент до 4 часов в рабочее окно. |

## 7) Безопасность и комплаенс

| ID | Статус | Решение |
|---|---|---|
| SEC-01 | answered | Секреты/API-ключи не требуются (только публичные данные). |
| SEC-02 | answered | Требования к audit/retention не заданы. |
| SEC-03 | answered | Регуляторные ограничения не заданы. |

## 8) Приёмка релиза

| ID | Статус | Решение |
|---|---|---|
| ACC-01 | answered | v1.1 ready, если: (1) p95 latency ≤500ms на тестовом прогоне, (2) stale-share ≤50%, (3) snapshot публикуется атомарно не реже 1 раза/мин в активной фазе рынка. |
| ACC-02 | answered | Обязательные интеграционные тесты: (1) получение котировок со всех 4 источников, (2) нормализация symbol/time, (3) запись snapshot с `# version: 1`, (4) восстановление после принудительного разрыва WS. |
| ACC-03 | answered | Финальный approver v1.1: владелец продукта/репозитория (requester) после успешного `make test` и проверки snapshot-артефактов. |

---

## Официальные источники (проверено для Day-1)
- Binance Spot API docs: https://developers.binance.com/docs/binance-spot-api-docs
- Binance USDⓈ-M Futures docs: https://developers.binance.com/docs/derivatives/usds-margined-futures
- Binance WS limits (300 connections attempts / 5 min / IP): https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams
- Bybit v5 API docs: https://bybit-exchange.github.io/docs/v5/intro
- Bybit rate limit rules: https://bybit-exchange.github.io/docs/v5/rate-limit

## Что осталось для полного закрытия
1. ✅ Зафиксированы endpoints и лимиты API/WS (DATA-01, DATA-02).
2. ✅ Утверждены SHM размеры (`MAX_SLOTS`, `SLOT_SIZE`) (TECH-03).
3. ✅ Закрыт контракт данных `Quote` и версия snapshot (SCHEMA-01/02/04).
4. ✅ Утверждены observability-стек и on-call (OPS-02, OPS-04).
5. ✅ Утверждены критерии приёмки и ответственный за релиз (ACC-01/02/03).
