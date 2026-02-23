---
description: "Generate a PR description from staged/changed files"
tools: ["search/codebase", "execute/runInTerminal", "execute/getTerminalOutput", "read/terminalLastCommand", "read/terminalSelection", "web/githubRepo"]
---

Generate a pull request description for the current changes using the project's PR template.

## Steps

1. Check which files have been changed (staged or modified)
2. Analyze the changes to understand what was done and why
3. Fill in the PR template from `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description

**Related Issue**: Closes #XXX

## Keep / Change / Remove

- **Keep**:
- **Change**:
- **Remove**:

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Infrastructure/DevOps change

## Changes Made

- Change 1
- Change 2

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Tests pass locally (`uv run poe test`)
- [ ] Coverage maintained/improved (target: 80%+)

## Architecture Impact

- [ ] Cloud-neutral by default (no hard dependency on a single provider)
- [ ] Cost-aware default path (works locally or free/open-source tier)
- [ ] Extension points documented for future adapters/plugins

## Deprecation / Migration

- [ ] No deprecation impact
- [ ] If behavior changed, deprecation/migration notes were added to docs/release notes

## Checklist

- [ ] Linting passes (`uv run poe lint` ✓)
- [ ] Type checking passes (`uv run poe typecheck` ✓)
- [ ] Documentation updated (if applicable)
- [ ] Pre-commit hooks pass

## Notes for Reviewers
```

4. Check the appropriate boxes based on actual changes
5. Write a concise but complete description
6. Use conventional commit style for the summary line
