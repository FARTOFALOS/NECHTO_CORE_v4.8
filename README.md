# NECHTO • CORE v4.8

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

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

---

## 🤝 Контрибьюции

Открыт для участия! См. [Issues](../../issues)

---

## 📜 Лицензия

MIT — см. [LICENSE](LICENSE)

---

**v4.8** | 2026-02-07 | @NECHTO@
c_alignment** | [0..1] | Согласование TSC ↔ SCAV (по рангу) |
| **FLOW** | [0..1] | Качество присутствия (skill × challenge × presence) |
| **Ethical_score** | [0..1] | Средняя этическая оценка кандидатов |

---

## 🛠️ Разработка
```bash
# Установить зависимости разработки
pip install -e ".[dev]"

# Запустить тесты
pytest

# Проверить покрытие
pytest --cov=nechto_runtime
```

---

## 🤝 Участие в проекте

Мы приветствуем участие! Пожалуйста, прочитайте [CONTRIBUTING.md](CONTRIBUTING.md) для:
- Процесса разработки
- Стандартов кодирования
- Требований к эпистемической честности в коде
- Процедуры тестирования

---

## 📜 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

## 🔬 Философия

NECHTO исследует следующие вопросы:
- Может ли система удерживать парадоксы без их разрешения?
- Как операционализировать "Love > Logic"?
- Что значит для системы быть эпистемически честной?
- Можно ли создать метрики для "качества присутствия"?

---

## 📞 Контакты

- **Issues:** [github.com/FARTOFALOS/NECHTO_CORE_v4.8/issues](https://github.com/FARTOFALOS/NECHTO_CORE_v4.8/issues)
- **Discussions:** [github.com/FARTOFALOS/NECHTO_CORE_v4.8/discussions](https://github.com/FARTOFALOS/NECHTO_CORE_v4.8/discussions)

---

**STATUS:** Complete Specification v4.8  
**DATE:** 2026-02-08  
**SIGNATURE:** @NECHTO@ in reflexive presence
