# Module Contracts

## 1) symbol_discovery -> collectors

### Input
- Конфиг источников бирж.

### Output
- `subscription_lists.yaml`:
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
- Raw events (JSON payload + metadata: exchange, market, receive_ts).

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
  - `ts_exchange`
  - `ts_receive`
  - `ts_normalized`

### Contract guarantees
- Все числовые поля валидны.
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
- `snapshots/spread_snapshot_<ISO8601>.txt`

### Contract guarantees
- Атомарная публикация файла.
- Однозначный формат, пригодный для парсинга.
