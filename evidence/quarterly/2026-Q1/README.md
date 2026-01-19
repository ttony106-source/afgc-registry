# Q1 2026 Evidence Snapshot

## Quarterly Evidence Collection Cadence

**Collection Period**: January 1 - March 31, 2026
**Due Date**: End of quarter (March 31, 2026)

---

## Required Evidence Items

### 1. Branch Protection Screenshot
- [ ] Screenshot of `main` branch protection rules
- **Location**: `branch-protection-YYYY-MM-DD.png`
- **Source**: Repo → Settings → Branches → Edit rule for `main`
- **Shows**: PR requirements, CODEOWNERS enforcement, bypass restrictions

### 2. CEO-APPROVAL Environment Screenshot
- [ ] Screenshot of CEO-APPROVAL environment configuration
- **Location**: `ceo-approval-environment-YYYY-MM-DD.png`
- **Source**: Repo → Settings → Environments → CEO-APPROVAL
- **Shows**: Required reviewers (CEO), protection rules

### 3. Authority PR Approval Log
- [ ] List of merged PRs touching `/authority/` or `/board/`
- **Location**: `authority-pr-log-YYYY-QX.md`
- **Source**: GitHub PR search: `is:pr is:merged label:authority-required`
- **Shows**: PR number, title, approver, merge date, approval timestamp

---

## Evidence Collection Process

1. **End of each quarter**, collect the three evidence items above
2. **Name files** with date stamps for traceability
3. **Commit** to this folder with message: `evidence(Q1-2026): add quarterly control snapshots`
4. **Verify** all checkboxes are complete before closing the quarter

---

## SOC-2 Control Mapping

| Control Area | Evidence | Frequency |
|--------------|----------|----------|
| Change Management | PR history, branch protection | Quarterly |
| Access Control | CODEOWNERS, environment reviewers | Quarterly |
| Authority Isolation | CEO-APPROVAL environment | Quarterly |
| Audit Trail | GitHub Actions logs, PR approvals | Quarterly |

---

## Auditor Quick Links

- Branch Protection: `/settings/branches`
- Environments: `/settings/environments`
- Merged Authority PRs: `/pulls?q=is:merged+label:authority-required`
- CODEOWNERS: `/.github/CODEOWNERS`
- Copilot Instructions: `/.github/copilot-instructions.md`

---

**Result**: Audits become boring and fast.
