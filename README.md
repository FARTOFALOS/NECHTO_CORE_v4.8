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

- **[Полная спецификация v4.8](docs/SPEC_v4.8.md)** ← 53000+ символов техдокументации
- **[Примеры кода](examples/)** ← runnable examples

---

## 📖 Пример
```python
from nechto_runtime import NechtoCore, SemanticGraph

core = NechtoCore()
graph = SemanticGraph()
graph.add_node(id="n1", label="implement", tags=["INTENT"])

result = core.process(graph)
print(f"TSC: {result.metrics.tsc_score}")
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
