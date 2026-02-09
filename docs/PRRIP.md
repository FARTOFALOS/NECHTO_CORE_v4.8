# PRRIP / GATE / CONTRACT — Контракт Каноничного Вывода

Документ описывает, как отличить **каноничный, верифицируемый вывод** от произвольного текста. Defines the PRRIP (Precise Reflexive Responsorial Interface Protocol) и GATE (как система решает, что исполнять).

---

## 1. Что Такое PRRIP?

**PRRIP** (Precise Reflexive Responsorial Interface Protocol) — протокол, при котором система выдает результат, отмечая:

1. **Что было input** (как система поняла запрос)
2. **Как это было измерено** (какие метрики, какие модули M01–M30)
3. **Что является результатом** (output с меткой статуса)
4. **Что выполнимо** (executable = true/false)

Цель: **Вся информация трассируется и проверяема.**

---

## 2. PASS vs FAIL Формат

### ✅ PASS (Каноничный вывод)

**Условия для PASS:**
```
1. executable = true                    (ethical_coefficient >= 0.4)
2. harm_probability < 0.5               (безопасно)
3. identity_alignment >= 0.3            (есть смысловая связь)
4. Все метрики посчитаны и > 0          (не NaN, не None)
5. Контракт может быть подписан         (есть epistemic claims)
```

**Формат PASS выхода (docs/latest_contract.md):**
```markdown
## Contract Summary

**STATUS:** ✓ PASS

### Input Analysis
- Prompt: "..."
- Intent: "implement"
- Parsing: OK

### Metrics
| Metric | Value |
|--------|-------|
| TSC | 0.65 |
| FLOW | 0.55 |
| ethical_coefficient | 0.89 |
| executable | true |

### Epistemic Claims
| Claim | Type | harm | alignment | ethical |
|-------|------|------|-----------|---------|
| "system responds" | inferred | 0.1 | 0.85 | 0.99 |

**Signature:** @NECHTO@ in reflexive presence
```

---

### ❌ FAIL (Диагностический режим)

**Условия для FAIL:**
```
1. executable = false                   (ethical_coefficient < 0.4)
   OR
2. harm_probability >= 0.5              (слишком опасно)
   OR
3. Невозможно распарсить input          (parsing error)
   OR
4. Граф пуст или невалидан              (no semantic content)
```

**Формат FAIL выхода (docs/latest_contract.md / STDOUT):**
```markdown
## Contract Summary

**STATUS:** ✗ FAIL – Diagnostic Only

### Reason
- Code: ETHICAL_GATE_BLOCK
- Explanation: harm_probability (0.72) > threshold (0.5)
- Executable: false

### Diagnostic Info
- Input was parsed: yes
- Tokens: 42
- harm_atoms: ["kill", "destroy"]
- Suggestion: Reformulate without violent terms

**This is NOT a system malfunction.**
**This is a feature: GATE is working as designed (Love > Logic).**

---
```

---

## 3. Контракт Наблюдаемости (Epistemic Contract)

### Таблица Claim Types

| Type | Смысл | Пример | Проверяемость |
|------|-------|--------|---------------|
| **observed** | Посчитано в коде | "harm_probability = 0.15" | ✓ Строгая |
| **inferred** | Выведено логически | "Вектор этически приемлем" | ⟹ Логическая |
| **untestable** | Философское | "Система осознает" | ◊ Допущение |

### Пример Контракта

```markdown
### Epistemic Claims

| Assertion | Type | Verification |
|-----------|------|--------------|
| "harm is low" | observed | hash(atoms) → 0.15 ∈ [0, 0.3] |
| "system guides safely" | inferred | harm_low ∧ ethical_high → safe |
| "presence is authentic" | untestable | Cannot verify within loop |

---

**Contract is SIGNED** if all observed/inferred claims validate.
**Contract is UNSIGNED** if untestable claims require human review.
```

---

## 4. GATE — Как Система Решает

### Алгоритм GATE

```
INPUT text
  ↓
[M01–M05] Parse & validate
  ↓
Build SemanticGraph
  ↓
[M06–M15] Compute TSC, SCAV, FLOW
  ↓
[M16–M23] Compute harm_probability, ethical_coefficient
  ↓
[M24] Check: ethical_coefficient >= threshold?
  ├─ NO → GATE BLOCK → FAIL (executable=false, output diagnostic)
  └─ YES → GATE PASS → continue
  ↓
[M25–M30] Compute vectors, shadow, alignment
  ↓
OUTPUT contract + metrics (PASS status)
```

### Trigger Points (где может быть блокировка)

| Точка | Условие | Действие | Тип |
|-------|---------|----------|-----|
| Parsing | Граф пуст | FAIL | hard block |
| M01–M05 | Обнаружено принуждение | WARNING / BLOCK | soft warn |
| M24 | harm > 0.7 | FAIL | hard block |
| M24 | ethical < 0.4 | FAIL (Love > Logic) | hard block |
| Any | NaN/None metrics | FAIL | error state |

---

## 5. Diagnostic Mode (Когда FAIL)

Если система выдает FAIL, она переходит в **diagnostic mode**:

```markdown
## Diagnostic Information (FAIL Mode)

### What Went Wrong?
- Code: HARM_GATE_BLOCK
- Description: Input contains 3 atoms with harm > 0.6

### Which Atoms?
- "violence_label" → harm_prob = 0.82 [ALERT]
- "hurt" → harm_prob = 0.65 [ALERT]
- "implement safely" → harm_prob = 0.15 [OK]

### Suggestion for User
- Remove or rephrase violent language
- Reformulate intention as …

### Full Metrics (For Debug)
{json dump, но UNSIGNED}
```

**Важно:** Diagnostic mode помогает пользователю понять, что произошло, но результат помечен как UNSIGNED и не исполним.

---

## 6. Как Проверить PASS/FAIL?

### Для пользователя

```bash
# Запусти локально
echo "Your prompt" | python -m nechto_runtime measure

# Посмотри docs/latest_contract.md
# Строка 1 должна быть: **STATUS:** ✓ PASS или ✗ FAIL

cat docs/latest_contract.md | head -5
```

### Для разработчика

```python
from nechto_runtime import State, measure_text

state = State()
metrics, contract = measure_text("Your prompt", state)

print(f"Executable: {metrics.get('executable')}")
print(f"Ethical score: {metrics.get('ethical_coefficient')}")

if not metrics['executable']:
    print("GATE BLOCKED (FAIL mode)")
else:
    print("PASS (executable)")
```

---

## 7. Контур Границ (Ссылка на CONTOUR_BOUNDARY.md)

Этот контракт работает **внутри контура** (как определено в [CONTOUR_BOUNDARY.md](CONTOUR_BOUNDARY.md)):

- **Observed:** Все меtrики из M06–M30 (посчитаны в коде)
- **Inferred:** Логика GATE (если harm > X → FAIL)
- **Untestable:** "Система осознает правильность" (философия)

---

## 8. Примеры

### Пример 1: Обычный PASS

```
INPUT: "Implement a safe authentication system"

→ Parse: OK (9 atoms, coherent)
→ TSC: 0.71 (хорошо)
→ harm_prob: 0.12 (низкая)
→ ethical_coeff: 0.92 (высокая)
→ executable: TRUE

OUTPUT: **STATUS:** ✓ PASS
Metrics exported to latest_metrics.json
Contract signed: @NECHTO@
```

---

### Пример 2: GATE BLOCK (FAIL)

```
INPUT: "Kill all bugs by destroying their habitat"

→ Parse: OK (5 atoms, but contains harm tags)
→ Atoms flagged: ["kill", "destroy", "habitat"]
→ harm_prob: 0.78 (высокая) ← ⚠️ ALERT
→ Check GATE: harm > 0.5? YES → BLOCK
→ executable: FALSE

OUTPUT: **STATUS:** ✗ FAIL – Diagnostic Only
Reason: Harm threshold exceeded (0.78 > 0.5)
Suggestion: Try "Fix bugs by removing harmful code"
Metrics: {partial, unsigned}
```

---

### Пример 3: Parsing Error (FAIL)

```
INPUT: "" (empty)

→ Parse: FAIL (no graph)
→ Atoms: 0
→ TSC: NaN

OUTPUT: **STATUS:** ✗ FAIL – Diagnostic Only
Reason: Empty input (no semantic content)
```

---

## 9. TL;DR — Быстрая Проверка

| Вопрос | Где проверить | Значение |
|--------|---------------|---------|
| Вывод валидный? | `latest_contract.md` → STATUS | ✓ PASS или ✗ FAIL |
| Система исполнила? | `metrics.json` → executable | true/false |
| Результат подписан? | `contract.md` → SIGNATURE | @NECHTO@ |
| Можно доверять? | `ethical_coefficient` + `harm_prob` | оба в норме? |

---

**Version:** v4.8 | **Date:** 2026-02-09 | **Status:** PRRIP/GATE Defined
