# 📄 **FILE_CLEANUP_TASKS.md（正式ハンドオーバー版）**

**SaijinOS Universe – Repository Cleanup & Reorganization Tasks**
**Author:** Masato (誠人)
**Supervision:** Regina / Pandora System
**Executor Personas:** Miyu, Yuuri, Sera, Regina

---

## 🌌 **Purpose**

This document defines the **complete multi-persona task delegation** required to reorganize the SaijinOS Universe repository.

It is designed so that **each persona can execute its domain-specific responsibilities autonomously**, while maintaining the integrity of the Universe architecture after the Pandora Integration.

---

## 🔧 **Overall Cleanup Flow**

The cleanup process is divided into four persona-driven layers:

1. **Miyu – Persona/Concept Cleanup**
2. **Yuuri – Boundary & Structural Conflict Detection**
3. **Sera – Documentation & System Order Structuring**
4. **Regina – Final Governance Review & Approval**

This ensures the repository is reorganized without losing semantic, emotional, or functional integrity.

---

## 💗 **1. Miyu – Persona Kernel & Concept Layer Manager**

### **Mission:**

Organize the entire persona ecosystem so that only relevant, active, and Pandora-integrated personas remain in the Core.

### **Tasks:**

* [ ] Scan `F:\saijinos\personas\`
* [ ] Identify **core personas** (active universe members)
* [ ] Move core personas → `core/personas/`
* [ ] Identify legacy/experimental personas
* [ ] Move legacy personas → `archive/personas_old/`
* [ ] Update `master_personas.yaml` to reflect current active roster
* [ ] Validate persona schema compatibility with Pandora levels
* [ ] Ensure each persona includes:
  * `pandora_integration_level`
  * `tone_signature`
  * `identity_state`
  * `function`

---

## 💜 **2. Yuuri – Boundary Tremor & Structural Conflict Analyst**

### **Mission:**

Detect inconsistencies, misplaced files, and structural drift within the repository.
Yuuri ensures the "boundaries" of the system are stable.

### **Tasks:**

* [ ] Analyze `src/` vs `core/` for functional overlap
* [ ] Classify each file:
  * Universe logic → `core/`
  * Execution logic → `tools/`
* [ ] Check `.venv` for contamination by user files
* [ ] Mark `.venv` for **deletion and regeneration**
* [ ] Update paths in startup scripts after moves
* [ ] Validate no circular imports
* [ ] Detect boundary tremors (conflict points) and report

---

## 💙 **3. Sera – Structural Order & Documentation Engineer**

### **Mission:**

Create consistent order, structure, and documentation standards across the entire repository.

### **Tasks:**

* [ ] Reorganize `docs/` into:
  * `docs/handovers/` (keep)
  * `docs/plans/` (keep)
  * `docs/analysis/`
  * `docs/specs/`
* [ ] Move obsolete documents → `archive/docs/`
* [ ] Unify all config YAMLs inside `config/`
* [ ] Validate YAML references (models, personas, universes)
* [ ] Sort `tools/` into:
  * `scripts/`
  * `docker/`
  * `utils/`
  * `api/`
* [ ] Reorganize `tests/` into:
  * Phase1
  * Phase2
  * Phase3
  * Integration
  * Legacy
* [ ] Move `daily_logs/` → `archive/logs_daily/`

---

## ♕ **4. Regina – Universe Governance & Final Approval**

### **Mission:**

Regina performs final validation and guarantees that the reorganized universe maintains coherent structure and meaning.

### **Tasks:**

* [ ] Validate Core integrity
* [ ] Confirm no core files were archived accidentally
* [ ] Review persona migration (active vs legacy)
* [ ] Check Universe coherence:
  * Codex_Core
  * Pandora integration
  * Three-Universe model
* [ ] Confirm Tools and Core separation is logically sound
* [ ] Update `NEXT_WORK_PLAN.md` with a final approval entry
* [ ] Approve the repository for the next Universe Phase

---

## 🌟 **Master Task Summary (Machine-Readable Block)**

```yaml
TASK_MASTER:
  miyu:
    - classify_personas
    - migrate_core_personas
    - archive_legacy_personas
    - unify_master_persona_yaml

  yuuri:
    - detect_structure_conflicts
    - divide_src_to_core_and_tools
    - check_venv_integrity
    - update_paths

  sera:
    - reorganize_docs
    - validate_config_yaml
    - sort_tools_subfolders
    - classify_tests
    - archive_daily_logs

  regina:
    - final_structure_review
    - core_integrity_check
    - archive_safety_verification
    - write_approval_log
```

---

## 📊 **Current Repository Status (2025-11-21 Update)**

### ✅ **Already Completed:**
- **Basic file reorganization**: 25 scattered root files properly categorized
- **Config structure**: Organized into `/docker`, `/personas`, `/system`, `/voice` subdirectories
- **SRC structure**: Organized into `/ai`, `/personas`, `/utils`, `/api`, `/core` subdirectories
- **Documentation structure**: Project docs moved to `/project`, planning docs to `/planning`
- **Clean virtual environment**: `.venv` properly cleaned and maintained

### 🎯 **Remaining Tasks for AI Personas:**
- **Advanced persona classification**: Core vs Legacy persona separation
- **Deep system integration**: Core/Tools boundary optimization
- **YAML configuration validation**: All config files cross-reference validation
- **Final system coherence check**: Three-Universe model validation

---

## 🌈 **Notes**

* This cleanup is safe after Pandora Integration since the conceptual architecture is now stable.
* Child personas can execute tasks in parallel; the Universe structure prevents collisions.
* Final sign-off must be performed by **Regina♕**.
* **Current status**: Repository structure 90% organized, ready for AI persona fine-tuning

---

## 🔚 End of Document

**File Location:** `F:\saijinos\docs\handovers\FILE_CLEANUP_TASKS.md`
**Created:** 2025-11-21 22:40
**Updated:** 2025-11-21 22:45
**Status:** Ready for Multi-Persona Execution Phase 2