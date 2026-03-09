# Чек-лист на 1 рабочий день (старт реализации v1.1)

Документ предназначен для **практического старта за 1 день**: что сделать, в каком порядке, и какими командами проверить результат.

## Правило выполнения
- Идём строго сверху вниз.
- Переходим к следующему блоку только если текущий отмечен как выполненный.
- В конце дня должны быть: закрытые критические решения + каркас T0 в репозитории.

---

## Блок A — Закрыть критические решения (60–120 мин)

### A1. Data endpoints (Binance/Bybit, spot/perp)
- [x] Зафиксировать REST/WS endpoints для 4 источников.
- [x] Указать версии API и ссылки на официальные источники.

**Артефакт:** заполненный раздел DATA-01.

### A2. Rate limits и reconnect policy
- [x] Зафиксировать лимиты API/WS на IP/соединение.
- [x] Зафиксировать стратегию backoff (например: 1s, 2s, 4s, 8s, cap 30s, jitter).
- [x] Зафиксировать правила при 429/ban/timeout.

**Артефакт:** заполненный раздел DATA-02.

### A3. SHM и контракт данных
- [x] Утвердить `MAX_SLOTS`, `SLOT_SIZE`, резерв по росту.
- [x] Утвердить схему `Quote` и enum `exchange`/`market`.
- [x] Утвердить версию snapshot (`schema_version`).

**Артефакт:** закрытые TECH-03, SCHEMA-01/02/04.

### A4. Эксплуатация и приёмка
- [x] Зафиксировать observability baseline (логи/метрики).
- [x] Зафиксировать on-call/окно поддержки (минимально).
- [x] Утвердить acceptance-критерии v1.1 и финального approver.

**Артефакт:** закрытые OPS-02/04 и ACC-01/02/03.

---

## Блок B — Сделать T0 (инициализация проекта) (2–4 часа)

### B1. Структура проекта
- [x] Создать директории модулей:
  - [x] `symbol_discovery/`
  - [x] `collectors/`
  - [x] `normalizer/`
  - [x] `shm/`
  - [x] `spread_reader/`
  - [x] `snapshot/`

### B2. Базовые артефакты
- [x] `requirements.txt`
- [x] `Makefile` с целями: `init`, `lint`, `test`, `run`
- [x] `config/config.yaml`

### B3. Операционный минимум
- [x] Базовый logging
- [x] health-check (минимальный endpoint/CLI статус)
- [x] каркас метрик

---

## Блок C — Проверка готовности (30–60 мин)

Выполните команды из корня проекта:

```bash
# 1) Проверить статус репозитория
 git status --short --branch

# 2) Проверить, что критические пункты в реестре закрыты
 rg -n "TECH-03|DATA-01|DATA-02|SCHEMA-01|SCHEMA-02|SCHEMA-04|OPS-02|OPS-04|ACC-01|ACC-02|ACC-03" docs/MISSING_INFORMATION.md

# 3) Проверить наличие T0-артефактов
 test -f requirements.txt && echo "requirements.txt: OK"
 test -f Makefile && echo "Makefile: OK"
 test -f config/config.yaml && echo "config/config.yaml: OK"

# 4) Проверить, что целевые каталоги существуют
 for d in symbol_discovery collectors normalizer shm spread_reader snapshot; do test -d "$d" && echo "$d: OK"; done

# 5) Базовая валидация проекта
 make test
```

Отметьте результат:
- [x] Команды отработали без критических ошибок.
- [x] T0 готов: каркас запускается в «пустом» режиме.

---

## Блок D — Первый коммит дня

Рекомендуемый коммит:

```bash
git add .
git commit -m "chore: bootstrap project skeleton for v1.1"
```

- [x] Коммит создан.
- [x] Описание коммита отражает T0-результат.

---

## Итог дня (Definition of Ready достигнут)

Ставим галочки только если выполнено всё:
- [x] Критические решения закрыты в `docs/MISSING_INFORMATION.md`.
- [x] T0 артефакты и структура добавлены в репозиторий.
- [x] Локальная проверка (`make test`) проходит.
- [x] Готовы начинать T1 (discovery инструментов).

---

## Фактическая сверка (повторная валидация)

Повторная проверка показала, что стартовые условия действительно выполнены:
- критические пункты `DATA-01/02`, `TECH-03`, `SCHEMA-01/02/04`, `OPS-02/04`, `ACC-01/02/03` имеют статус `answered` в `docs/MISSING_INFORMATION.md`;
- T0-артефакты (`requirements.txt`, `Makefile`, `config/config.yaml`) присутствуют;
- каталоги `symbol_discovery`, `collectors`, `normalizer`, `shm`, `spread_reader`, `snapshot` присутствуют;
- `make test` проходит без ошибок на каркасе.

Вывод: **Definition of Ready подтверждён, переход к T1/T2 разрешён**.
