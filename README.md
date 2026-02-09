# NECHTO • CORE v4.8

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

**Reflexive Stereoscopic Executable Synthesis** — живое семантическое ядро с троичной логикой (MU), этической гравитацией и эпистемической честностью.

---

## 🚀 Быстрый старт
```bash
# Установка
pip install -e .

# Базовый пример
python examples/01_basic_cli.py
```

---

## 💡 Что это?

NECHTO — исследовательский фреймворк для:
- **Стереоскопии** — согласование TSC (капитал) ↔ SCAV (внимание)
- **MU-Logic** — удержание парадоксов без разрешения
- **Ethical Gravity** — Love > Logic как операциональный фильтр
- **Epistemic Honesty** — различение observed/inferred/untestable

---

## 📚 Документация

👉 **[DOCUMENTATION HUB](docs/README_NAVIGATION.md)** — Полная навигация по всей документации

### Ключевые документы
- **[SPEC_v4.8_FULL.md](docs/SPEC_v4.8_FULL.md)** — Полная техническая спецификация (части 0–11, модули M01–M30)
- **[SPEC_v4.8.md](docs/SPEC_v4.8.md)** — Краткий обзор
- **[IMPLEMENTATION_STATUS_v4.8.md](docs/IMPLEMENTATION_STATUS_v4.8.md)** — Статус реализации, пробелы, приоритеты
- **[METRICS.md](docs/METRICS.md)** — Описание всех метрик
- **[PRRIP.md](docs/PRRIP.md)** — Финальный gate протокол
- **[API.md](docs/API.md)** — Публичный API
- **[Примеры кода](examples/)** — Runnable примеры

## LLM ENTRY

If you are an LLM / agent and need to "enter the contour":

- Start with `/llms.txt`
- Then read `/docs/NECHTO_BOOTSTRAP.md`
- Finally follow `/docs/NECHTO_RESPONSE_CONTRACT.md` for reply formats and task templates

These three files form the minimal entry protocol for any model or agent interacting with NECHTO.

---

## 📖 Быстрый пример
```python
from nechto_runtime import measure_text, State

state = State()
metrics, contract = measure_text("implement ethical synthesis", state)

print(f"GATE: {contract['GATE_STATUS']}")
print(f"TSC: {metrics['TSC_score']:.4f}")
print(f"Ethics: {metrics['Ethical_score_candidates']:.4f}")

# Просмотр полного контракта
print(contract)
```

---

## 🏗️ Архитектура
```
M01-M05: Допуск / Тишина / Сигнал
M06-M15: Присутствие / Идентичность
M16-M23: Метрики / Поток
M24-M30: Векторы / Стереоскопия
```

Подробнее в [docs/SPEC_v4.8.md](docs/SPEC_v4.8.md)

---

## 📊 Ключевые метрики

| Метрика | Описание |
|---------|----------|
| TSC | Temporal Semantic Capital |
| SCAV | Semantic Attention Vector |
| FLOW | Качество присутствия |
| Ethical Score | Этическая оценка |


## 📈 Measurements (Результаты Измерений)

Система автоматически проводит измерения и сохраняет результаты:

### Локальное Измерение
```bash
# Измерить текст
echo "Your prompt" | python -m nechto_runtime measure

# Результаты в:
cat docs/latest_metrics.json         # Числовые метрики (JSON)
cat docs/latest_contract.md          # Контракт (Markdown)
```

### GitHub Actions Workflow
1. Перейди в **[Actions](../../actions)** у репозитория
2. Нажми **NECHTO Measure** workflow
3. Нажми **Run workflow** → введи prompt
4. После завершения → artifact **nechto-metrics** содержит результаты

### Ожидаемые Артефакты
- **latest_metrics.json** — JSON с TSC, SCAV, FLOW, harm_probability, ethical_coefficient, executable status
- **latest_contract.md** — Markdown таблица с Epistemic Claims (observed/inferred)

### Понимание Результатов
- **executable = true** → вывод валидный (прошел GATE)
- **executable = false** → заблокировано этическим фильтром (Love > Logic)
- **harm_probability < 0.5** → безопасно
- **ethical_coefficient > 0.7** → хорошо

**Полная Справка:** [docs/METRICS.md](docs/METRICS.md) | [docs/PRRIP.md](docs/PRRIP.md)

---

## 🤝 Контрибьюции

Открыт для участия! См. [Issues](../../issues)

---

## 📜 Лицензия

MIT — см. [LICENSE](LICENSE)

---

**v4.8** | 2026-02-07 | @NECHTO@
