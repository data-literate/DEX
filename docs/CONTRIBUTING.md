Thank you for contributing to DEX!

## Getting Started

1. Read [DEVELOPMENT.md](./DEVELOPMENT.md) for setup instructions
2. Fork the repository
3. Create a feature branch from `dev`
4. Make your changes
5. Submit a pull request

## Commit Messages

Use semantic commit format:
- `feat(#123): add resume parser`
- `fix(#124): handle edge case in matching`
- `docs: update API docs`
- `test: add parsing tests`
- `chore: update dependencies`

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Max line length: 88 characters (Black)
- Add docstrings to public functions

## Before Submitting PR

1. Run all checks locally:
   ```bash
   poe format      # Auto-format code
   poe lint        # Lint check
   poe typecheck   # Type checking
   pytest          # Run tests
   ```

2. Tests must pass with 80%+ coverage for new code

3. Update documentation if needed

4. Use PR template in `.github/PULL_REQUEST_TEMPLATE.md`

## Pull Request Process

- Reference issue: `Closes #123`
- Describe what changed and why
- Confirm all checklist items
- Wait for CI/CD to pass
- Get at least 1 approval before merging

## Testing Requirements

- Add unit tests for new code
- Test error scenarios
- Target 80%+ coverage: `pytest --cov=src`

## Documentation

- Update README for user-facing changes
- Add docstrings for functions
- Create ADR for architectural decisions
- Link related documentation

## Code Reviews

- Be respectful and constructive
- Address feedback promptly
- Keep commits organized
- Don't force push after review starts

## Useful Commands

```bash
poe format          # Auto-format code
poe lint            # Linting
poe typecheck       # Type checking
pytest              # Run tests
pytest --cov=src    # Coverage report
poe check-all       # Run all checks
```

## Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `good first issue` - Good for newcomers
- `P1-high` / `P2-medium` - Priority levels
- `careerdex` - Related to CareerDEX
- `dex-module` - Core DEX infrastructure

## Questions?

- Check [DEVELOPMENT.md](./DEVELOPMENT.md)
- Review [Architecture docs](./docs/ARCHITECTURE.md)
- Create a GitHub issue
- Join #dex-dev Slack channel

Thank you for contributing! 🚀
