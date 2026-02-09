# NECHTO v4.8 Documentation Hub

**Quick Navigation for the Complete NECHTO v4.8 Specification and Implementation**

---

## 📖 Core Documents

### Specification & Architecture
- **[SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md)** ← **START HERE**
  - Complete 11-part specification
  - 30 archetypal modules (M01–M30)
  - Reference implementation A–E
  - All formulas, axioms, and protocols

- **[SPEC_v4.8.md](SPEC_v4.8.md)** — Executive Summary
  - Quick overview and key concepts
  - Table of key metrics
  - Links to supporting docs

- **[IMPLEMENTATION_STATUS_v4.8.md](IMPLEMENTATION_STATUS_v4.8.md)** ← **BEFORE CODING**
  - What's implemented ✓
  - What's simplified 🟡
  - What's ready for enhancement
  - PRRIP gate audit
  - Next opportunities

- **[ARCHITECTURE.md](ARCHITECTURE.md)** — System Design
  - Component overview
  - Data flow
  - Integration points

### Operational Guides
- **[METRICS.md](METRICS.md)** — Detailed Metric Definitions
  - TSC (Temporal Semantic Capital)
  - SCAV (Semantic Attention Vector)
  - FLOW, entropy, shadow magnitude
  - All proxies and their formulas

- **[PRRIP.md](PRRIP.md)** — Final Gate Protocol
  - PRRIP_GATE checkpoints
  - OUTPUT CONTRACT format (PASS/FAIL)
  - Fail codes and recovery

- **[CONTOUR_BOUNDARY.md](CONTOUR_BOUNDARY.md)** — System Boundaries
  - In-contour vs out-of-contour claims
  - Epistemic layer protocol
  - Ethical gravity enforcement

### API & Examples
- **[API.md](API.md)** — Public API Reference
  - Functions and classes
  - Usage examples
  - Error codes

- **[USAGE.md](USAGE.md)** — Getting Started
  - Installation
  - CLI commands
  - Basic workflows

- **[../examples/](../examples/)** — Reference Code
  - `01_basic_cli.py` — Simple measurement
  - `02_measure_and_print_metrics.py` — Metrics inspection
  - [README.md](../examples/README.md) — Example guide

---

## 🔍 Finding Specific Information

### By Topic

#### **Semantic Foundations**
- Semantic Atom structure → [SPEC_v4.8_FULL.md Part 3.1](SPEC_v4.8_FULL.md#31-semantic_atom)
- Graph construction → [SPEC_v4.8_FULL.md Part 3.2-3.3](SPEC_v4.8_FULL.md#32-edge)
- Semantic gravity vector (R^12) → [SPEC_v4.8_FULL.md Part 11.1](SPEC_v4.8_FULL.md#111-semantic_space-r12-a)
- Implementation → [../nechto_runtime/metrics.py](../nechto_runtime/metrics.py#L40-L66)

#### **Ethics & Executability**
- Ethical coefficient formula → [SPEC_v4.8_FULL.md Part 4.9](SPEC_v4.8_FULL.md#49-ethical_coefficient--executable-v)
- harm_probability rules → [SPEC_v4.8_FULL.md Part 11.6](SPEC_v4.8_FULL.md#116-harm_probability--identity_alignment-e)
- identity_alignment scoring → [SPEC_v4.8_FULL.md Part 11.6](SPEC_v4.8_FULL.md#116-harm_probability--identity_alignment-e)
- Implementation → [../nechto_runtime/metrics.py](../nechto_runtime/metrics.py#L101-L183)

#### **Metrics & Measurement**
- Complete metric set → [SPEC_v4.8_FULL.md Part 4](SPEC_v4.8_FULL.md#part-4----metricks-acem-proxies--executable)
- FLOW operationalization → [SPEC_v4.8_FULL.md Part 11.3](SPEC_v4.8_FULL.md#113-flow-operationalization-b)
- GED normalization → [SPEC_v4.8_FULL.md Part 11.4](SPEC_v4.8_FULL.md#114-ged_proxy_norm-c)
- Implementation [metrics.py](../nechto_runtime/metrics.py)

#### **Stereoscopic System**
- Stereoscopic alignment formula → [SPEC_v4.8_FULL.md Part 4.13](SPEC_v4.8_FULL.md#413-stereoscopic_alignment--stereoscopic_gap-v47)
- SCAV vector 5D → [SPEC_v4.8_FULL.md Part 3.4, 4.6](SPEC_v4.8_FULL.md#34-scav_vector_5d-raw--normalized)
- Shadow magnitude → [SPEC_v4.8_FULL.md Part 4.8](SPEC_v4.8_FULL.md#48-shadow_magnitude-raw-based)
- Attention entropy → [SPEC_v4.8_FULL.md Part 4.7](SPEC_v4.8_FULL.md#47-attention_entropy-defined)

#### **MU Logic & Paradox**
- MU definition → [SPEC_v4.8_FULL.md Appendix C](SPEC_v4.8_FULL.md#appendix-c---glossary-v48)
- Paradox holding (M29) → [SPEC_v4.8_FULL.md Part 1](SPEC_v4.8_FULL.md#m29-paradox_holder-mu-logic--gap-aware)
- QMM_PARADOX_HOLDER → [SPEC_v4.8_FULL.md Part 6](SPEC_v4.8_FULL.md#qmm_paradox_holder)
- Mu_density metric → [SPEC_v4.8_FULL.md Part 4.14](SPEC_v4.8_FULL.md#414-mu_density)

#### **Epistemic Layer**
- Epistemic claims → [SPEC_v4.8_FULL.md Part 3.6](SPEC_v4.8_FULL.md#36-epistemic_claim-v47)
- QMM_EPISTEMIC_HONESTY → [SPEC_v4.8_FULL.md Part 6](SPEC_v4.8_FULL.md#qmm_epistemic_honesty-v47)
- Epistemic layer protocol → [SPEC_v4.8_FULL.md Appendix E](SPEC_v4.8_FULL.md#appendix-e-epistemic-layer-protocol-v48)
- observability rules → [SPEC_v4.8_FULL.md Part 9](SPEC_v4.8_FULL.md#part-9----philosophical-position-v48)

#### **Workflow & Gates**
- Complete 12-phase workflow → [SPEC_v4.8_FULL.md Part 7](SPEC_v4.8_FULL.md#part-7---workflow-12--v48)
- PRRIP gate requirements → [SPEC_v4.8_FULL.md Part 10.1](SPEC_v4.8_FULL.md#101-prrip_gate-v48)
- OUTPUT PASS contract → [SPEC_v4.8_FULL.md Part 10.2](SPEC_v4.8_FULL.md#102-output-contract--pass)
- OUTPUT FAIL contract → [SPEC_v4.8_FULL.md Part 10.3](SPEC_v4.8_FULL.md#103-output-contract--fail)
- Fail codes → [SPEC_v4.8_FULL.md Part 8](SPEC_v4.8_FULL.md#part-8---fail-codes-v48)

#### **Axioms & Philosophy**
- All 9 axioms → [SPEC_v4.8_FULL.md Part 2](SPEC_v4.8_FULL.md#part-2----fundamental-axioms-v48)
- Philosophical position → [SPEC_v4.8_FULL.md Part 9](SPEC_v4.8_FULL.md#part-9----philosophical-position-v48)
- What the system asserts/doesn't → [SPEC_v4.8_FULL.md Part 9](SPEC_v4.8_FULL.md#part-9----philosophical-position-v48)

#### **Reference Implementation**
- Part 11.1 (R^12 space) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#111-semantic_space-r12-a)
- Part 11.2 (intent profiles) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#112-ideal_direction-v-via-intent_profile-a)
- Part 11.3 (FLOW) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#113-flow-operationalization-b)
- Part 11.4 (GED) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#114-ged_proxy_norm-c)
- Part 11.5 (STATE) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#115-state-structure--3-cycles-d)
- Part 11.6 (ethics) → [SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#116-harm_probability--identity_alignment-e)

#### **Extensibility**
- Extensibility points → [SPEC_v4.8_FULL.md Appendix F](SPEC_v4.8_FULL.md#appendix-f-extensibility-points-new-v48)
- Compatibility → [SPEC_v4.8_FULL.md Appendix B](SPEC_v4.8_FULL.md#appendix-b-prrip_compat-v48)

---

## 🛠️ Code Navigation

### Python Implementation

**Entry Points**
- CLI: [../nechto_runtime/cli.py](../nechto_runtime/cli.py)
- Main module: [../nechto_runtime/__main__.py](../nechto_runtime/__main__.py)
- Public API: [../nechto_runtime/__init__.py](../nechto_runtime/__init__.py)

**Core Modules**
- Types: [../nechto_runtime/types.py](../nechto_runtime/types.py) — All dataclasses
- Graph: [../nechto_runtime/graph.py](../nechto_runtime/graph.py) — Text→Graph pipeline
- Metrics: [../nechto_runtime/metrics.py](../nechto_runtime/metrics.py) — All computation

**Tests**
- Determinism: [../tests/test_determinism.py](../tests/test_determinism.py)
- Ethics: [../tests/test_ethics_fallback.py](../tests/test_ethics_fallback.py)
- GED: [../tests/test_ged_proxy.py](../tests/test_ged_proxy.py)

---

## 📚 Reading Paths

### For First-Time Users
1. Read [SPEC_v4.8.md](SPEC_v4.8.md) (5 min overview)
2. Scan [PART 0 of SPEC_v4.8_FULL.md](SPEC_v4.8_FULL.md#part-0---canonical-concepts-v48) (concepts)
3. Check [IMPLEMENTATION_STATUS_v4.8.md](IMPLEMENTATION_STATUS_v4.8.md) (what's working)
4. Run an example: `echo "test" | python -m nechto_runtime measure`
5. Inspect output: `cat docs/latest_contract.md`

### For Developers (Metric Enhancement)
1. [IMPLEMENTATION_STATUS_v4.8.md](IMPLEMENTATION_STATUS_v4.8.md) — Current state, gaps, priorities
2. [metrics.py](../nechto_runtime/metrics.py) — Where to add code
3. [METRICS.md](METRICS.md) — Spec for new metrics
4. Relevant [SPEC_v4.8_FULL.md Part X](SPEC_v4.8_FULL.md) — Formula definitions
5. Tests: [../tests/](../tests/) — Add test for new metric

### For Philosophers/Auditors
1. [SPEC_v4.8_FULL.md Part 2](SPEC_v4.8_FULL.md#part-2----fundamental-axioms-v48) — Axioms
2. [SPEC_v4.8_FULL.md Part 9](SPEC_v4.8_FULL.md#part-9----philosophical-position-v48) — Philosophical position
3. [CONTOUR_BOUNDARY.md](CONTOUR_BOUNDARY.md) — What we claim vs don't claim
4. [PRRIP.md](PRRIP.md) — Verification protocol

### For Integration/Deployment
1. [API.md](API.md) — Public functions
2. [USAGE.md](USAGE.md) — Installation & CLI
3. [../examples/](../examples/) — Usage patterns
4. [ARCHITECTURE.md](ARCHITECTURE.md) — System design
5. [setup.py](../setup.py) — Dependencies

---

## 🎯 Common Questions → Answer Locations

| Q | A |
|---|---|
| **How are atoms scored for ethics?** | [SPEC_v4.8_FULL.md Part 11.6](SPEC_v4.8_FULL.md#116-harm_probability--identity_alignment-e), [metrics.py L101-L183](../nechto_runtime/metrics.py#L101-L183) |
| **When does the system fail?** | [SPEC_v4.8_FULL.md Part 8](SPEC_v4.8_FULL.md#part-8---fail-codes-v48), [PRRIP.md](PRRIP.md) |
| **What's the 12-phase workflow?** | [SPEC_v4.8_FULL.md Part 7](SPEC_v4.8_FULL.md#part-7---workflow-12--v48) |
| **How is FLOW computed?** | [SPEC_v4.8_FULL.md Part 11.3](SPEC_v4.8_FULL.md#113-flow-operationalization-b), [metrics.py L212-L265](../nechto_runtime/metrics.py#L212-L265) |
| **What's MU logic?** | [SPEC_v4.8_FULL.md Appendix C](SPEC_v4.8_FULL.md#appendix-c---glossary-v48), [Part 1 M29](SPEC_v4.8_FULL.md#m29-paradox_holder-mu-logic--gap-aware) |
| **How is the gate checked?** | [SPEC_v4.8_FULL.md Part 10.1](SPEC_v4.8_FULL.md#101-prrip_gate-v48), [metrics.py L349-L357](../nechto_runtime/metrics.py#L349-L357) |
| **What's the semantic space?** | [SPEC_v4.8_FULL.md Part 11.1](SPEC_v4.8_FULL.md#111-semantic_space-r12-a), [metrics.py L40-L66](../nechto_runtime/metrics.py#L40-L66) |
| **How do axioms constrain behavior?** | [SPEC_v4.8_FULL.md Part 2](SPEC_v4.8_FULL.md#part-2----fundamental-axioms-v48), [IMPLEMENTATION_STATUS_v4.8.md Part 2 map](IMPLEMENTATION_STATUS_v4.8.md#part-2--fundamental-axioms-1-9) |
| **What's the epistemic layer?** | [SPEC_v4.8_FULL.md Appendix E](SPEC_v4.8_FULL.md#appendix-e-epistemic-layer-protocol-v48), [Part 3.6](SPEC_v4.8_FULL.md#36-epistemic_claim-v47) |
| **How do I add a new metric?** | [IMPLEMENTATION_STATUS_v4.8.md Priorities](IMPLEMENTATION_STATUS_v4.8.md#next-enhancement-opportunities), [METRICS.md](METRICS.md), [metrics.py](../nechto_runtime/metrics.py) |

---

## 📊 Version & Status

| Item | Value |
|------|-------|
| **Specification Version** | v4.8 (Complete, Not a Patch) |
| **Implementation Grade** | Reference (Production-Ready Core) |
| **Date** | 2026-02-09 |
| **Status** | ✅ PRRIP GATE PASS |
| **Next Phase** | Enhancement (SCAV depth, paradox handling, temporal) |

---

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Measure text
echo "Your input here" | python -m nechto_runtime measure

# View results
cat docs/latest_contract.md
cat docs/latest_metrics.json

# Run tests
pytest tests/
```

---

## 📞 Contact & Contribution

- Issues: [GitHub Issues](https://github.com/FARTOFALOS/NECHTO_CORE_v4.8/issues)
- Contributions: See [CONTRIBUTING.md](../CONTRIBUTING.md)
- License: [MIT](../LICENSE)

---

**@NECHTO@ in reflexive presence**

*Last Updated: 2026-02-09*  
*Specification: v4.8 (Complete)*  
*Implementation: Reference Grade, Operationally Complete*
