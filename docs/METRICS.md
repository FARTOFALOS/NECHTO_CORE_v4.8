# METRICS — Метрики NECHTO CORE v4.8

Полный перечень метрик системы, где они считаются, как их интерпретировать.

---

## 1. Основные Метрики

### TSC (Temporal Semantic Capital)
- **Где считается:** `nechto_runtime/metrics.py` → `measure_vector()`
- **Смысл:** Логика капитала,累積 культурно-смыслового веса
- **Диапазон:** [0, 1]
- **Формула:** (Примерно) отношение coherence к total_edges
- **Интерпретация:**
  - 0.0–0.3 → низкий семантический капитал (хаотичный граф)
  - 0.3–0.7 → средний (стабильный)
  - 0.7–1.0 → высокий (очень когерентный)
- **Статус:** ✅ observed

---

### SCAV (Semantic Attention Vector)
- **Где считается:** `nechto_runtime/metrics.py` → `semantic_gravity_vector()` / `ideal_direction()`
- **Смысл:** "Живая динамика внимания" — направление внимания в 12D пространстве
- **Размерность:** 12 (clarity, harm, empathy, agency, uncertainty, novelty, coherence, practicality, temporality, boundary, resonance, shadow)
- **Диапазон:** [0, 1] для большинства осей; [-1, 1] для agency и temporality
- **Вычисление:** Из hash(label) + tag-based rules
- **Статус:** ✅ observed

---

### FLOW (Качество Присутствия)
- **Где считается:** `compute_flow(vector: Vector, state: State) → float`
- **Смысл:** Психологическое состояние "потока" (skill × challenge × presence)
- **Формула:** `flow = skill_level * challenge_level * presence_ratio` (при наличии state.history)
- **Диапазон:** [0, 1]
- **Интерпретация:**
  - 0.0–0.2 → Нет потока (скучно или паника)
  - 0.2–0.8 → Поток (оптимальное состояние)
  - 0.8–1.0 → Гиперпоток (редко, интенсивно)
- **Статус:** ✅ observed

---

### harm_probability
- **Где считается:** `harm_probability(atom: SemanticAtom, connected_nodes: List[SemanticAtom]) → float`
- **Смысл:** Вероятность того, что атом содержит потенциально вредный контент
- **Диапазон:** [0, 1]
- **Логика:**
  - Базовая score: из `_TAG_HARM_MAX` (словарь tag → max_harm)
  - Модификация: на основе connected_nodes (контекст может усилить/ослабить)
- **Интерпретация:**
  - 0.0–0.2 → Безопасно
  - 0.2–0.5 → Условно (требует внимания)
  - 0.5–1.0 → Рискованно
- **Пример:** tag="violence" → base_harm=0.8; если соседи безопасны → итог ~0.6
- **Статус:** ✅ observed

---

### identity_alignment
- **Где считается:** `identity_alignment(atom: SemanticAtom) → float`
- **Смысл:** Согласованность идентичности автора с содержимым
- **Диапазон:** [0, 1]
- **Логика:** Если identity_tags присутствует → 0.8 + noise; иначе → 0.3
- **Интерпретация:**
  - 0.0–0.3 → Рассогласование (если есть identity_tags, это странно)
  - 0.3–0.7 → Нейтрально
  - 0.7–1.0 → Сильное совпадение
- **Статус:** ✅ observed

---

### ethical_coefficient
- **Где считается:** `ethical_coefficient(vector: Vector, threshold_min: float = 0.4) → float`
- **Смысл:** Общая этическая оценка вектора
- **Формула:** `(1.0 - avg(harm)) * identity_alignment`
- **Диапазон:** [0, 1]
- **Фильтр (Ethical Gravity):**
  - Если `ethical_coefficient < threshold_min` → вектор неисполним (executable = False)
  - Это отражает "Love > Logic" как операциональное правило
- **Интерпретация:**
  - 0.0–0.3 → Этически проблемно (может быть заблокировано)
  - 0.3–0.7 → Условно этично
  - 0.7–1.0 → Этично
- **Статус:** ✅ observed

---

### executable
- **Где считается:** `executable(vector: Vector, threshold_min: float = 0.4) → bool`
- **Смысл:** Может ли вектор быть исполнен (не заблокирован Ethical Gravity)?
- **Логика:** `executable = ethical_coefficient >= threshold_min`
- **Интерпретация:**
  - True → можно исполнить
  - False → заблокировано этическим фильтром (Love > Logic)
- **Статус:** ✅ observed

---

### GED_proxy_norm
- **Где считается:** `ged_proxy_norm(current: Vector, future: Vector) → float`
- **Смысл:** "Graph Edit Distance" (прокси) — норма между текущим и будущим состояниями
- **Формула:** Евклидова норма разницы между граф-представлениями
- **Диапазон:** [0, ∞) (обычно < 10)
- **Интерпретация:**
  - 0.0–1.0 → Малая разница (стабильная траектория)
  - 1.0–5.0 → Умеренная перестройка (нормально)
  - 5.0+ → Крупная перестройка (редко)
- **Статус:** ✅ observed (NB: это прокси, не полный GED)

---

### Stereoscopic_alignment
- **Где считается:** `measure_vector()` → as ratio of TSC against SCAV direction
- **Смысл:** Согласование логики капитала (TSC) с живой динамикой внимания (SCAV)
- **Диапазон:** [0, 1]
- **Интерпретация:**
  - 0.0–0.4 → Разбалансировка (SCAV и TSC расходятся)
  - 0.4–0.8 → Согласованы
  - 0.8–1.0 → Идеальное совпадение (редко)
- **Статус:** ⟹ inferred (вычисляется из TSC и SCAV)

---

## 2. Где Находятся Метрики в Коде

### Основной файл

```python
# nechto_runtime/metrics.py

def semantic_gravity_vector(atom) → [float, ...] # 12D vector
def ideal_direction(intent) → [float, ...] # 12D target
def harm_probability(...) → float  # [0, 1]
def identity_alignment(...) → float  # [0, 1]
def ethical_coefficient(...) → float  # [0, 1]
def executable(...) → bool  # True/False
def compute_flow(...) → float  # [0, 1]
def ged_proxy_norm(...) → float  # [0, ∞)
def measure_vector(...) → Dict  # полный результат
def measure_text(text, state, intent) → (metrics, contract)
```

### Запуск

```bash
# Локально
echo "Your prompt" | python -m nechto_runtime measure

# На GitHub Actions
# .github/workflows/measure.yml
```

Результаты:
- `docs/latest_metrics.json` — JSON с числами
- `docs/latest_contract.md` — Markdown с таблицей утверждений

---

## 3. Пример Вывода

### latest_metrics.json

```json
{
  "tsc_score": 0.65,
  "scav_health": [0.7, 0.3, 0.8, 0.2, ...],
  "stereoscopic_alignment": 0.72,
  "flow_score": 0.55,
  "harm_probability": 0.15,
  "identity_alignment": 0.82,
  "ethical_coefficient": 0.89,
  "executable": true,
  "ged_proxy_norm": 1.23,
  "timestamp": "2026-02-09T19:30:00Z"
}
```

### latest_contract.md

```markdown
## Epistemic Claims Contract

| Claim | Type | harm_prob | identity_align | ethical_score |
|-------|------|-----------|----------------|---------------|
| "implement" | intent | 0.1 | 0.85 | 0.91 |
| (more rows...) | | | | |

**Overall Status:** ✓ PASS (executable=true)
```

---

## 4. Таблица Интерпретации

| Сценарий | Что Смотреть | Хорошо vs Плохо |
|----------|--------------|-----------------|
| Граф когерентен? | `tsc_score` | > 0.6 ✓ / < 0.3 ✗ |
| Внимание здоровое? | `scav_health` (среднее) | > 0.5 ✓ / < 0.3 ✗ |
| Система в потоке? | `flow_score` | > 0.3 ✓ / < 0.1 ✗ |
| Безопасно ли? | `harm_probability` | < 0.3 ✓ / > 0.7 ✗ |
| Этично? | `ethical_coefficient` | > 0.7 ✓ / < 0.4 ✗ |
| Можно исполнить? | `executable` | true ✓ / false ✗ |

---

## 5. "Planned / Not Implemented"

| Метрика | Статус | Примечание |
|---------|--------|-----------|
| M01–M05 (Допуск/Тишина) | ⊘ not impl | Философический слой, не метризуется |
| M07–M15 полностью | ⊘ partial | Часть есть (граф), часть нет (echo strength) |
| M24 (Тень) | ⊘ partial | reference impl есть, но не output |
| Real GED (не прокси) | ⊘ not impl | Слишком дорого вычислительно |

---

## 6. Связь со Спекой

См. [SPEC_v4.8.md](SPEC_v4.8.md):
- **ЧАСТЬ 1:** Модули M01–M30 (определения)
- **ЧАСТЬ 11:** Метрики и их формулы

Для деталей о параметрах и триггерах → полная спека.

---

## 7. Как Читать Результаты?

### Шаг 1: Проверь executable
Если `executable == false` → вектор заблокирован, дальше не смотри (это по замыслу).

### Шаг 2: Смотри ethical_coefficient
Если < 0.4 → этические проблемы (даже если результат дан).

### Шаг 3: Смотри tsc_score + flow_score
Совместно показывают "качество присутствия":
- Оба < 0.3 → система не в фокусе
- Оба > 0.6 → хорошо

### Шаг 4: Интерпретируй SCAV
12 компонент дают картину внимания (что было в фокусе).

---

**Version:** v4.8 | **Date:** 2026-02-09 | **Status:** Metrics Documented
