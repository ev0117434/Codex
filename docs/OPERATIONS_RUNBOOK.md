# Operations Runbook (v1.1)

## Startup order
1. `symbol_discovery`
2. `shm_init` (если не инициализирован)
3. `collectors`
4. `normalizer`
5. `spread_reader`

## Runtime checks
- Обновляется ли `subscription_lists.yaml`.
- Есть ли входящий WS-трафик по 4 источникам.
- Растут ли counters `normalized_quotes_total`.
- Генерируются ли snapshots с ожидаемым интервалом.
- Валидны ли имена snapshot-файлов (`spread_snapshot_YYYYMMDDTHHMMSSZ.txt`).

## Failure scenarios

### 1) WS disconnect storm
**Симптомы:** частые reconnect, рост lag/stale.  
**Действия:** увеличить backoff, проверить сеть/лимиты API, подтвердить актуальность подписок.

### 2) SHM version mismatch
**Симптомы:** reader/writer не читают/пишут.  
**Действия:** остановить процессы, запустить `shm_cleaner`, затем `shm_init`, перезапустить пайплайн.

### 3) Snapshot generation stalled
**Симптомы:** нет новых файлов в `snapshots/`.  
**Действия:** проверить health spread_reader, ошибки stale, доступность SHM и права записи.

## Recovery procedure
1. Graceful stop всех процессов.
2. Очистка/переинициализация SHM при необходимости.
3. Холодный запуск в startup order.
4. Проверка первых N snapshots и метрик свежести.

## SLO / Alert table (v1.1 baseline)

| Компонент | SLO | Метрика | Alert-порог |
|---|---|---|---|
| `collectors` | reconnect recovery p95 ≤ 30s | `collector_reconnect_duration_seconds` | p95 > 30s в течение 10 мин |
| `normalizer` | parse error rate < 1% | `normalize_errors_total / raw_events_total` | > 1% в течение 5 мин |
| `shm` | write/read lag p95 ≤ 5ms | `shm_write_read_lag_ms` | p95 > 5ms в течение 10 мин |
| `spread_reader` | snapshot latency p95 ≤ interval + 20% | `snapshot_latency_ms` | p95 > target в течение 10 мин |
| end-to-end | stale-share ≤ 50% (эквивалентно fresh ≥ 50%) | `stale_records_ratio` | > 50% в течение 15 мин |

## Minimal SLO draft
- Freshness: stale-share <= 50% (в соответствии с SLO-02 и реестром решений).
- Snapshot latency: p95 не хуже целевого интервала + 20%.
- Service availability: целевое значение 100% (SLO-03), фактическая операционная модель — best effort для single-host v1.1.
