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
- `ts_exchange`: int (ms/ns, зависит от источника; после normalize приводится к ns)
- `ts_receive`: int (ns)
- `ts_normalized`: int (ns)

## Spread formula
`spread = (best_ask_futures - best_bid_spot) / best_bid_spot * 100`

## Rules
1. `best_bid_spot > 0`.
2. Обе котировки должны быть свежими: `age < STALENESS_THRESHOLD`.
3. Для stale/отсутствия данных выводим `N/A`.
4. Отрицательный spread допустим и не обрезается.

## Snapshot format

### File naming
`spread_snapshot_<ISO8601>.txt`

### Write strategy
1. Запись во временный файл.
2. `os.rename(temp, final)` — атомарная публикация.

### Record example
`BTC-USDT  0.1523  43521.50  43454.75  binance  binance  no`

Поля:
- `SYMBOL`
- `SPREAD%`
- `ASK_FUT`
- `BID_SPOT`
- `FUT_EXCH`
- `SPOT_EXCH`
- `STALE`
