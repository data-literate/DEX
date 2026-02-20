---
description: "Review code against project standards and checklists"
tools: ["search/codebase"]
---

Review the code in ${file} against DataEngineX project standards.

## Check against these criteria

Reference `.github/CHECKLISTS.md` and `.github/copilot-instructions.md` for full details.

### Must-check items:
- [ ] Type hints on all public functions (params + return)
- [ ] No hardcoded secrets, API keys, passwords, tokens
- [ ] No bare `except:` — catch specific exceptions with context
- [ ] Errors logged with structured key-value pairs (not f-strings)
- [ ] `from __future__ import annotations` present
- [ ] Functions under 50 lines, max 4 parameters
- [ ] Tests exist for new functionality
- [ ] No `print()` or stdlib `logging` — use loguru/structlog

### API-specific (if applicable):
- [ ] `response_model=` declared on endpoints
- [ ] Input validation via Pydantic models
- [ ] Consistent error format from `errors.py`
- [ ] Auth check on protected endpoints

### Data pipeline-specific (if applicable):
- [ ] Pipeline is idempotent
- [ ] Processing counts logged
- [ ] Schema validated at entry point

## Output format
List issues found with file location, severity (critical/warning/info), and suggested fix.
