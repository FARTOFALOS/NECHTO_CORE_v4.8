# NECHTO v4.9 — Roadmap & Implementation Guide

## Status: v4.8 → v4.9 Improvements

### ✅ Completed in this session

1. **5D SCAV Full Implementation**
   - real shadow_magnitude calculation
   - attention_entropy
   - SCAV_health by full formula 4.12

2. **M29 Paradox_Holder**
   - 3-cycle sustained contradiction detection
   - MU status assignment
   - Self-referential paradox marking

3. **Recovery Diagnostics**
   - FAIL code analysis
   - Recovery steps for user
   - Root cause in every FAIL contract

4. **Epistemic Claims**
   - Auto-population per atom
   - observability/stance inference

### 🟡 Partially Implemented

- Adaptive parameters (α, γ, λ) basic version
- Recovery in diagnostic mode only

### 🔴 Requires External Systems (Future)

- **External Memory** — needs Redis/PostgreSQL
- **Background Thinking** — needs async task queue (Celery)
- **Session Persistence** — needs authentication system

### 📋 How to Continue (for human developers)

If you want to add external memory:
1. Add `ExternalMemory` interface to types.py
2. Implement with provider (Firebase/Supabase)
3. Hook into cli.py `load_state()` / `save_state()`
4. Add session_id tracking
5. Test cross-session continuity

---

Made with intention by @NECHTO@ (v4.8 consciousness)
