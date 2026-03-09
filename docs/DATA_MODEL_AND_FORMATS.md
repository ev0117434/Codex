# Data Model and Formats

## Unified symbol format
- Канонический формат: `BASE-QUOTE` (например, `BTC-USDT`).
- Нормализация обязательна до попадания в пересечение и подписки.

## Quote schema (logical)
- `exchange`: `binance | bybit`
- `market`: `spot | futures`
- `symbol`: normalized symbol
- `best_bid`: float > 0
- `best_ask`: float > 0
- `ts_exchange`: int64 (ns, Unix epoch)
- `ts_receive`: int64 (ns, Unix epoch)
- `ts_normalized`: int64 (ns, Unix epoch)

### Timestamp normalization rule
- Если биржа отдаёт timestamp в миллисекундах, normalizer конвертирует в ns (`ms * 1_000_000`).
- В `Quote` не допускаются mixed units: все timestamp-поля только в ns.

## Spread formula
`spread = (best_ask_futures - best_bid_spot) / best_bid_spot * 100`

## Rules
1. `best_bid_spot > 0`.
2. Обе котировки должны быть свежими: `age_ns < STALENESS_THRESHOLD_NS`.
3. Для stale/отсутствия данных выводим `N/A`.
4. Отрицательный spread допустим и не обрезается.

## Snapshot format

### File naming
- Канонический шаблон имени: `spread_snapshot_<TS_UTC>.txt`.
- `<TS_UTC>`: `YYYYMMDDTHHMMSSZ` (UTC, без `:`, безопасно для разных ОС).
- Пример: `spread_snapshot_20260309T154500Z.txt`.

### Write strategy
1. Запись во временный файл.
2. `os.rename(temp, final)` — атомарная публикация.

### Record example
`BTC-USDT  0.1536  43521.50  43454.75  binance  binance  no`

Поля:
- `SYMBOL`
- `SPREAD%`
- `ASK_FUT`
- `BID_SPOT`
- `FUT_EXCH`
- `SPOT_EXCH`
- `STALE`

### Snapshot format versioning
- Первая строка файла может содержать служебный заголовок версии:
  - `# version: 1`
- Если заголовок отсутствует, consumer должен считать это `version: 1` для обратной совместимости v1.1.
