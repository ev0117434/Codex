# Operations Runbook (v1.1)

## Startup order
1. `symbol_discovery`
2. `collectors`
3. `normalizer`
4. `shm_init` (если не инициализирован)
5. `spread_reader`

## Runtime checks
- Обновляется ли `subscription_lists.yaml`.
- Есть ли входящий WS-трафик по 4 источникам.
- Растут ли counters `normalized_quotes_total`.
- Генерируются ли snapshots с ожидаемым интервалом.

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
3. Холодный запуск в startup-order.
4. Проверка первых N snapshots и метрик свежести.

## Minimal SLO draft
- Freshness: >= 95% записей не stale в нормальном сетевом режиме.
- Snapshot latency: p95 не хуже целевого интервала + 20%.
- Service availability: best effort для single-host v1.1.
