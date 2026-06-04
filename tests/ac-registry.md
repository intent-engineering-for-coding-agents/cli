# AC ID Registry

One row per component prefix. The counter column is monotone — never reuse a number
after deletion. When adding a new scenario to a spec, increment the counter and record
the new max here.

| Prefix | Component / Spec | Max used | Spec file |
|---|---|---|---|
| `SCAFFOLD` | scaffold-command — `iec init` core | 016 | `openspec/specs/scaffold-command/` |
| `VENDOR` | vendor-generators — `--with-claude`, `--with-gemini` | 008 | `openspec/specs/vendor-generators/` |
| `CHKRSL` | check-result-model — CheckResult dataclass | 007 | `openspec/specs/check-result-model/` |
| `CHKREG` | checker-registry — Registry class | 011 | `openspec/specs/checker-registry/` |
| `CHKCLI` | check-cli — `iec check` command | 010 | `openspec/specs/check-cli/` |
| `AGEX` | agents-exists | 003 | `openspec/specs/agents-exists/` |
| `AGSZ` | agents-size | 006 | `openspec/specs/agents-size/` |
| `AGLN` | agents-links | 006 | `openspec/specs/agents-links/` |
| `DRME` | docs-readme-exists | 006 | `openspec/specs/docs-readme-exists/` |
| `DINE` | docs-index-exists | 006 | `openspec/specs/docs-index-exists/` |
| `DINS` | docs-index-stale | 007 | `openspec/specs/docs-index-stale/` |
| `DISO` | docs-index-scope | 008 | `openspec/specs/docs-index-scope/` |
| `ADRF` | adr-format | 015 | `openspec/specs/adr-format/` |
| `ADRI` | adr-index | 007 | `openspec/specs/adr-index/` |
| `ACID` | spec-ac-ids | 005 | `openspec/specs/spec-ac-ids/` |
| `STCT` | spec-test-category | 005 | `openspec/specs/spec-test-category/` |
| `SPSZ` | spec-size | 006 | `openspec/specs/spec-size/` |
| `FLSZ` | file-size | 007 | `openspec/specs/file-size/` |
| `AHUB` | agents-hub-structure | 006 | `openspec/specs/agents-hub-structure/` |
| `SECR` | secrets | 006 | `openspec/specs/secrets/` |
| `TRTC` | test-traceability | 011 | `openspec/specs/test-traceability/` |
| `TCOV` | test-coverage | 007 | `openspec/specs/test-coverage/` |
| `TSKC` | tasks-complete | 007 | `openspec/specs/tasks-complete/` |
| `CHGA` | change-archived | 007 | `openspec/specs/change-archived/` |
| `EVAL` | eval-cli — `iec eval` command | 017 | `openspec/changes/archive/2026-05-25-eval-command/` |
