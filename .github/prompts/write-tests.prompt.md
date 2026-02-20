---
description: "Write tests for the current file"
tools: ["search/codebase", "execute/runInTerminal", "execute/getTerminalOutput", "read/terminalLastCommand", "read/terminalSelection"]
---

Write tests for the code in ${file}.

## Rules

1. **Location** — Place tests in `tests/unit/test_<module>.py` (match module name)
2. **Style**:
   - `asyncio_mode = "auto"` — do NOT add `@pytest.mark.asyncio`
   - Use `@pytest.mark.parametrize` for input variations
   - Group related tests in `Test<Component>` classes
   - Name: `test_<what_it_tests>` — descriptive, not implementation-tied
3. **Test Clients**:
   - Sync API tests: `TestClient` from Starlette
   - Async API tests: `httpx.AsyncClient` with `ASGITransport`
   - Create `TestClient` locally in each test file (conftest.py is minimal)
4. **Coverage**:
   - Happy path + error paths + edge cases (empty, None, boundary)
   - Mock external services only, not code under test
   - Use `tmp_path` for file operations
5. **Verify** — Run `poe test-unit` to confirm tests pass

Follow patterns in existing tests under `tests/unit/`.
