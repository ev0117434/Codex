# Assumptions and Limits (v1.1)

## Assumptions
1. **Single-host deployment**: все процессы работают на одном хосте.
2. **Clock discipline**: NTP/chrony включены; допустимый drift системных часов не более 100 мс.
3. **Time source policy**:
   - для timestamp в данных — Unix epoch ns;
   - для измерения длительностей и таймаутов — monotonic clock.
4. **Network conditions**: периодические флуктуации допустимы, длительные partition не являются целевым сценарием v1.1.
5. **Exchange API limits**: лимиты бирж соблюдаются; при throttling система деградирует контролируемо.

## Limits
1. Нет встроенного long-term storage и replay в v1.1.
2. Нет multi-host HA в v1.1.
3. Snapshot — pull-ориентированный артефакт без query API.
4. При потере обоих рынков для символа значение в snapshot для этого символа становится `N/A`.
