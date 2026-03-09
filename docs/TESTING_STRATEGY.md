# Testing Strategy

## Цель
Подтвердить, что простая архитектура v1.1 корректна, устойчива к сбоям и наблюдаема.

## Unit tests
1. Symbol normalization:
   - `BTCUSDT -> BTC-USDT`
   - edge-cases/invalid input
2. Exchange parsers:
   - корректное извлечение bid/ask/timestamps
   - поведение на неполных payload
3. Spread formula:
   - положительный, нулевой, отрицательный spread
   - `best_bid_spot <= 0`
4. SHM seqlock:
   - writer/reader consistency
   - race-like сценарии

## Integration tests
1. Discovery -> subscription file generation.
2. Collector raw event -> normalizer -> SHM write.
3. SHM read -> spread -> snapshot file.
4. Snapshot atomicity (temp + rename).
5. Snapshot naming format validation (`YYYYMMDDTHHMMSSZ`).
6. Contract check: all `Quote` timestamps are in ns.

## Resilience tests (smoke)
1. Принудительный WS reconnect.
2. Временное отсутствие одного из рынков.
3. Увеличение входного потока до N символов.

## Exit criteria for v1.1
- Критические unit/integration тесты зелёные.
- Snapshot не ломается при сетевых флуктуациях.
- Метрики и логи позволяют диагностировать отказ без дебага в коде.
