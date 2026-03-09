# Module Contracts

## 1) symbol_discovery -> collectors

### Input
- Конфиг источников бирж.

### Output
- `subscription_lists.yaml`:
  - `version: 1`
  - `generated_at_ns: <int64>`
  - `binance_spot: [symbols...]`
  - `binance_futures: [symbols...]`
  - `bybit_spot: [symbols...]`
  - `bybit_futures: [symbols...]`

### Contract guarantees
- Только активные символы.
- Символы в унифицированном формате.
- Полная перезапись файла в каждом цикле (без частичных апдейтов).

## 2) collectors -> normalizer

### Input
- WS stream по каждому источнику.

### Output
- Raw events (JSON payload + metadata: exchange, market, receive_ts_ns).

### Contract guarantees
- События не модифицируются collector-ом (кроме обогащения метаданными).
- Реконнекты прозрачны для downstream.

## 3) normalizer -> shm

### Input
- Raw event.

### Output
- `Quote`:
  - `exchange`
  - `market`
  - `symbol`
  - `best_bid`
  - `best_ask`
  - `ts_exchange` (int64 ns)
  - `ts_receive` (int64 ns)
  - `ts_normalized` (int64 ns)

### Contract guarantees
- Все числовые поля валидны.
- Timestamp-поля строго в ns.
- Некорректные сообщения отбрасываются с логированием причины.

## 4) shm -> spread_reader

### Input
- Последние `Quote` из SHM.

### Output
- Строки snapshot по символам.

### Contract guarantees
- Чтение только консистентных слотов.
- Для stale/отсутствующих данных — `N/A`.

## 5) spread_reader -> external consumers

### Output artifact
- `snapshots/spread_snapshot_YYYYMMDDTHHMMSSZ.txt`

### Contract guarantees
- Атомарная публикация файла.
- Однозначный формат, пригодный для парсинга.
- Опциональный заголовок версии `# version: 1`.
