# GitHub Project Management Setup Guide

This guide explains how to use GitHub for complete SDLC and project management for DEX.

## Overview

DEX uses GitHub's built-in features for project management:
- **GitHub Issues** - Track bugs, features, and tasks
- **GitHub Projects** - Kanban boards for sprint/epic tracking
- **Labels** - Categorize and prioritize work
- **Milestones** - Group issues for releases
- **Pull Requests** - Code review workflow

## Issue Templates

We provide three issue templates:

### 1. Bug Report (`bug_report.yml`)
Use for reporting bugs or unexpected behavior.
- Required fields: description, reproduction steps, expected vs actual behavior
- Automatically labeled with `bug`

### 2. Feature Request (`feature_request.yml`)
Use for proposing new features or enhancements.
- Includes priority and component selection
- Acceptance criteria section
- Automatically labeled with `enhancement`

### 3. Task/Chore (`task.yml`)
Use for non-feature work (refactoring, docs, config, etc.).
- Task type categorization
- Checklist support
- Automatically labeled with appropriate label

## Labels

### Priority Labels
Create these labels manually via GitHub UI:

```bash
gh label create "P0-critical" --description "Critical - blocks release" --color "B60205"
gh label create "P1-high" --description "High priority" --color "D93F0B"
gh label create "P2-medium" --description "Medium priority" --color "FBCA04"
gh label create "P3-low" --description "Low priority" --color "0E8A16"
```

### Component Labels (already exist)
- `python` - Python code changes
- `github_actions` - CI/CD workflow changes
- `dependencies` - Dependency updates
- `documentation` - Docs updates

### Type Labels (already exist)
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `question` - Further information needed
- `good first issue` - Good for newcomers

### Status Labels (create these)
```bash
gh label create "status:blocked" --description "Blocked by another issue" --color "D93F0B"
gh label create "status:in-progress" --description "Currently being worked on" --color "FBCA04"
gh label create "status:review" --description "Ready for review" --color "0E8A16"
```

### Environment Labels (create these)
```bash
gh label create "env:dev" --description "Affects dev environment" --color "C2E0C6"
gh label create "env:stage" --description "Affects stage environment" --color "BFD4F2"
gh label create "env:prod" --description "Affects production" --color "D73A4A"
```

## Creating a GitHub Project

### Option 1: Via GitHub CLI
```bash
# Requires authentication with project scope
gh auth refresh -s project

# Create a new project (Board view)
gh project create --owner data-literate --title "DEX Development" --format board
```

### Option 2: Via GitHub UI
1. Go to: https://github.com/orgs/data-literate/projects (or your user projects)
2. Click "New project"
3. Choose "Board" template
4. Name it "DEX Development" or "DEX Sprint Board"
5. Configure columns:
   - Backlog (no automation)
   - Todo (no automation)
   - In Progress (auto-move when issue assigned)
   - In Review (auto-move when PR opened)
   - Done (auto-move when issue closed)

### Link Repository to Project
1. Open the project
2. Settings → Linked repositories
3. Add `data-literate/DEX`

### Automation Rules
Configure auto-move rules:
- When issue **assigned** → move to "In Progress"
- When PR **opened** → move to "In Review"
- When issue **closed** → move to "Done"
- When PR **merged** → move to "Done"

## Milestones

Create milestones for releases:

```bash
# Via CLI
gh api repos/data-literate/DEX/milestones -f title="v1.0.0" -f description="Initial production release" -f due_on="2026-03-01T00:00:00Z"

# Or via GitHub UI
# https://github.com/data-literate/DEX/milestones/new
```

Example milestones:
- **v0.1.0** - MVP with basic API
- **v0.2.0** - ML pipeline integration
- **v1.0.0** - Production-ready release

## Workflow

### 1. Planning Phase
- Create issues for upcoming work
- Add to project backlog
- Assign priority labels (P0-P3)
- Assign to milestone
- Add component labels
- Estimate effort (use comments or custom fields)

### 2. Development Phase
- Move issue to "Todo" column
- Create feature branch: `git switch -c feat/issue-123-short-desc`
- Assign issue to yourself → auto-moves to "In Progress"
- Commit with references: `git commit -m "feat: add feature #123"`
- Push and open PR → auto-moves to "In Review"
- Link PR to issue: `Resolves #123` in PR description

### 3. Review Phase
- Request reviews from team
- Address feedback
- Ensure all checks pass (CI, Security, etc.)
- Get approval

### 4. Merge & Deploy
- Merge PR (squash preferred) → auto-closes issue
- Issue auto-moves to "Done"
- Deployments follow the CI/CD pipeline

See [CI/CD Pipeline](CI_CD.md) for deployment automation details.

### 5. Retrospective
- Review completed issues in milestone
- Close milestone when released
- Document learnings in issues/wiki

## Querying Issues

### Via GitHub CLI
```bash
# List open issues
gh issue list --state open

# List issues by label
gh issue list --label "P0-critical"
gh issue list --label "bug,env:prod"

# List issues in milestone
gh issue list --milestone "v1.0.0"

# List your assigned issues
gh issue list --assignee "@me"

# Search issues
gh issue list --search "API error"
```

### Via GitHub UI
- All issues: https://github.com/data-literate/DEX/issues
- Filter by label, milestone, assignee, author
- Save custom filters

## Best Practices

### Issue Creation
- **Be specific**: Clear, actionable description
- **Add context**: Link related issues, PRs, documentation
- **Set priority**: Use P0-P3 labels
- **Add labels**: Component, type, status, environment
- **Break down work**: Large issues should have checklists or sub-issues
- **Link to PRs**: Use "Resolves #123" in PR description

### Issue Management
- **Keep updated**: Comment with progress updates
- **Use assignees**: Assign to person actively working
- **Link dependencies**: Comment "Blocked by #456" and add label
- **Close when done**: Don't leave stale issues open
- **Reference in commits**: Use `#123` in commit messages

### Project Board
- **Review regularly**: Daily standup around project board
- **Keep columns updated**: Move cards manually if automation fails
- **Archive completed**: Move old done issues to archive
- **Triage backlog**: Regular backlog grooming sessions

### Pull Requests
- **Link to issue**: Always reference the issue number
- **Small PRs**: Easier to review, faster to merge
- **Good descriptions**: Explain what/why, not just how
- **Request reviews**: Don't wait for reviews to happen
- **Respond quickly**: Address review comments promptly

## Integration with CI/CD

CI/CD automation is documented in [CI/CD Pipeline](CI_CD.md). This guide focuses on project management mechanics.

## Useful Links

- **Repository**: https://github.com/data-literate/DEX
- **Issues**: https://github.com/data-literate/DEX/issues
- **Pull Requests**: https://github.com/data-literate/DEX/pulls
- **Projects**: https://github.com/orgs/data-literate/projects (or user projects)
- **Milestones**: https://github.com/data-literate/DEX/milestones
- **Labels**: https://github.com/data-literate/DEX/labels

## Getting Started Checklist

- [ ] Create issue templates (done ✅)
- [ ] Create additional labels (priority, status, environment)
- [ ] Create GitHub Project board
- [ ] Link repository to project
- [ ] Configure automation rules
- [ ] Create first milestone
- [ ] Create first issue using template
- [ ] Add issue to project board
- [ ] Start working and follow workflow

---

**See Also:**
- [SDLC Guide](SDLC.md) - Development lifecycle stages
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Main README](../Readme.md) - Repository overview
