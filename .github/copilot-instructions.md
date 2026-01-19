# CEO Authority Isolation Controls - Copilot Custom Instructions

## CORE PRINCIPLE
The CEO is NEVER pulled into execution. The CEO is ONLY invoked for explicit authority-binding actions.

## MANDATORY RULES FOR ALL COPILOT OPERATIONS

### 1. AUTHORITY SEGREGATION
- **NEVER** suggest changes that mix execution code with authority paths
- **NEVER** create PRs that touch `/authority/` or `/board/` alongside execution files
- **ALWAYS** maintain strict separation between:
  - `/execution/` - automation only (NO CEO involvement)
  - `/validation/` - checks, tests, linting
  - `/evidence/` - logs, hashes, manifests
  - `/authority/` - CEO-touch zone ONLY
  - `/board/` - board & trustee actions ONLY
  - `/archives/` - immutable releases

### 2. CEO PROTECTION RULES
- CEO (@ftony106-source) must **NEVER** be added as reviewer for execution PRs
- CEO must **ONLY** be requested for review on `/authority/**` or `/board/**` paths
- **NEVER** suggest bypassing CODEOWNERS rules
- **NEVER** suggest force-pushing to protected branches

### 3. PROHIBITED ACTIONS (NON-NEGOTIABLE)
Copilot must **NEVER** suggest or generate code that:
- Signs documents automatically
- Accepts contracts without human approval
- Triggers capital movement
- Acknowledges legal responsibility
- Bypasses MFA or authentication
- Stores CEO credentials
- Auto-approves authority-bound changes

### 4. WORKFLOW REQUIREMENTS
All generated workflows MUST:
- Run in non-privileged mode
- Use least-privilege tokens
- Produce immutable artifacts
- Generate logs and hashes
- Fail closed (no silent success)
- Pause at `AUTHORITY_REQUIRED` checkpoints
- Require explicit CEO approval for authority paths

### 5. PULL REQUEST RULES

#### For Execution PRs (Non-Authority):
- CEO must be **EXCLUDED** from reviewers
- Tests must pass
- Lint/security checks enforced
- Minimal diff validation
- No scope creep

#### For Authority-Bound PRs:
- Located **ONLY** in `/authority/` or `/board/`
- Single-purpose PR
- Explicit "Authority Impact" summary required
- CEO is **SOLE** approver
- Merge requires approval + audit log

### 6. EVIDENCE GENERATION
Every authority-touching operation must generate:
- Timestamp
- Actor identification
- Workflow ID
- Artifact hash (SHA-256)
- Decision summary
- Risk classification

### 7. FAILURE CONDITIONS
Immediately halt and alert if:
- CEO appears in execution PRs
- Automation attempts to touch `/authority/`
- Workflow executes without required approval
- Missing logs or hashes
- Permission boundaries are crossed

## EXECUTIVE RULE
**If GitHub did not prepare it, validate it, log it, and pause it - the CEO must not touch it.**

---
*This instruction set ensures SOC-2 aligned authority isolation and fiduciary protection.*
