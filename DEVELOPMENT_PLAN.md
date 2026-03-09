# План разработки: Crypto Spread Monitor (по base1.pdf)

## Цель
Собрать систему мониторинга спреда между spot и futures (Binance/Bybit) с пайплайном:
`symbol_discovery -> collectors -> normalizer -> POSIX SHM -> spread_reader -> snapshot`.

## Этап 0 — Подготовка и каркас
1. Создать структуру каталогов и модулей из раздела `7. Структура проекта`.
2. Добавить `requirements.txt`, `Makefile`, базовый `config/config.yaml`.
3. Настроить единый logging + базовые метрики + health-check endpoints/файлы.

## Этап 1 — Symbol Discovery
1. Исследовать и зафиксировать REST endpoints для:
   - Binance Spot/Futures
   - Bybit Spot/Futures
2. Реализовать адаптеры получения списка инструментов по 4 источникам.
3. Добавить фильтрацию «активных» инструментов (status/is_trading и эквиваленты).
4. Реализовать нормализацию символов в единый формат (`BASE-QUOTE`).
5. Реализовать логику пересечения символов между нужными рынками.
6. Формировать `subscription_lists.yaml` (4 списка подписок).
7. Добавить кэш discovery + периодический запуск `discovery_runner.py`.

## Этап 2 — Collectors (WebSocket)
1. Реализовать 4 коллектора best bid/ask:
   - binance_spot
   - binance_futures
   - bybit_spot
   - bybit_futures
2. Добавить подписку по спискам из `subscription_lists.yaml`.
3. Реализовать reconnect/backoff, heartbeat, ограничение нагрузки.
4. Складывать сырые события в внутреннюю очередь для normalizer.

## Этап 3 — Normalizer
1. Определить dataclass `Quote` (symbol, market, exchange, best_bid, best_ask, ts_exchange, ts_receive и т.д.).
2. Написать 4 парсера сырых WS-сообщений в единый `Quote`.
3. Добавить валидации (числа > 0, обязательные поля, timestamp).
4. Подготовить запись нормализованных котировок в SHM-слоты.

## Этап 4 — SHM слой
1. Реализовать layout сегмента `/csm_quotes_v1`:
   - Header (MAGIC, VERSION, MAX_SLOTS, SLOT_SIZE, created_ts_ns)
   - Slot-массив для котировок
2. Реализовать `shm_init.py` с безопасной переинициализацией по MAGIC/version.
3. Реализовать writer/reader с seqlock-протоколом:
   - writer: `seq_begin += 1` (odd) -> запись -> `seq_end = seq_begin` (even)
   - reader: читать только консистентные срезы.
4. Добавить `shm_cleaner.py` и диагностику состояния сегмента.

## Этап 5 — Spread Reader и snapshots
1. Реализовать формулу:
   `spread = (best_ask_futures - best_bid_spot) / best_bid_spot * 100%`.
2. Добавить правила:
   - проверка staleness (`age < STALENESS_THRESHOLD`)
   - `best_bid_spot > 0`
   - для stale/отсутствующих данных писать `N/A`
   - отрицательный spread не обрезать.
3. Реализовать атомарную запись snapshot:
   - temp-файл -> `os.rename()`
   - формат `spread_snapshot_<ISO8601>.txt`
4. Добавить периодический `spread_runner.py`.

## Этап 6 — Observability
1. Метрики по каждому этапу пайплайна:
   - задержка discovery
   - lag WS сообщений
   - время normalize/write/read
   - доля stale
   - количество reconnect/error
2. Структурированные логи с correlation fields (exchange/market/symbol).
3. Минимальные алерты на деградацию (рост stale, разрыв потока).

## Этап 7 — Тестирование
1. Unit-тесты:
   - нормализация символов
   - парсинг WS payload
   - формула spread
   - seqlock reader/writer edge cases
2. Интеграционные тесты:
   - discovery -> subscription file
   - collector -> normalizer -> SHM
   - SHM -> spread -> snapshot
3. Нагрузочный smoke-тест на N символов, проверка latency и стабильности.

## Этап 8 — Ввод в эксплуатацию
1. Подготовить runbook (запуск, ротация логов, очистка SHM, recovery).
2. Зафиксировать SLA/SLO (freshness, uptime, max snapshot latency).
3. Подготовить roadmap v1.2 (доп. биржи, хранение истории, UI/дашборд).

## Критерии готовности v1.1
- Discovery стабильно обновляет подписки для 4 источников.
- Collectors получают best bid/ask и выдерживают реконнекты.
- Normalizer пишет в SHM без гонок, reader читает консистентно.
- Snapshot генерируется атомарно и соответствует формату из спецификации.
- Метрики/логи позволяют локализовать проблемы по этапам пайплайна.
