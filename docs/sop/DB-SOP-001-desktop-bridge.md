# DESKTOP BRIDGE SOP
## Authority-Safe Execution for GUI-Locked Systems

| Field | Value |
|-------|-------|
| **Document ID** | DB-SOP-001 |
| **Status** | Active |
| **Effective Date** | January 19, 2026 |
| **Applies to** | Banking portals, DocuSign UI (non-API), Adobe Acrobat, MFA-locked systems |
| **CEO Role** | Authority only (never execution) |

---

## 1. PURPOSE

This SOP governs the last 10-15% of work that cannot be executed via APIs or GitHub Actions due to:
- MFA-locked portals
- UI-only workflows
- Legal identity requirements
- Regulator / bank constraints

> **The goal is not to automate authority.**
> **The goal is to remove everything except the authority moment.**

---

## 2. NON-NEGOTIABLE PRINCIPLE

```
The Desktop Bridge may transport work to the point of authority.
It may NEVER cross the authority line.
```

If a system requires:
- A signature
- An acknowledgement
- Acceptance of liability

**The CEO must perform exactly one deliberate action.**

---

## 3. DESKTOP BRIDGE MODES

### MODE A - API-FIRST (DEFAULT)

| Attribute | Value |
|-----------|-------|
| Use when | API available |
| Examples | DocuSign API, Stripe, Airtable, Cloudflare |
| CEO interaction | None |
| Risk | Low |
| Audit posture | Strong |

> If an API exists and you choose UI instead -> **policy violation**

### MODE B - HUMAN-ASSISTED DESKTOP (PREFERRED FOR BANKS)

| Role | Permissions |
|------|-------------|
| **Operator** | Prepare files, upload documents, navigate menus, pause at confirmation |
| **CEO** | Login, final review, single confirmation action, logout |

**Operator may NOT:**
- Enter credentials
- Click "Submit / Confirm / Sign"
- Acknowledge terms

> This mode is often safer than bots.

### MODE C - CONTROLLED RPA (LIMITED USE)

**Allowed only when:**
- UI path is stable
- Action is deterministic
- No judgment required

**RPA may:**
- Open applications
- Navigate to fixed screens
- Upload prepared artifacts
- Stop at authority screen

**RPA must NEVER:**
- Decide
- Sign
- Accept terms
- Bypass MFA
- Store credentials

**Mandatory controls:**
- Manual trigger only
- Time-boxed run
- Screen recording
- Immediate kill-switch

> If RPA cannot stop instantly -> **not allowed**

---

## 4. DESKTOP BRIDGE ENTRY CONDITIONS (HARD GATE)

A desktop session may **NOT** begin unless ALL are true:

- [ ] GitHub execution completed
- [ ] Evidence generated (hashes, manifests)
- [ ] Authority PR created or Issue logged
- [ ] CEO summary prepared (1 page max)
- [ ] Kill-switch verified

**If any condition is missing -> STOP**

---

## 5. CEO DESKTOP INTERACTION RULES

### The CEO MAY:
- Log in
- Review prepared screen
- Perform one authority action
- Log out

### The CEO must NOT:
- Navigate workflows
- Upload files
- Retry failed steps
- Troubleshoot UI
- Handle formatting issues

**If something breaks -> abort session**

---

## 6. KILL-SWITCH (MANDATORY)

Every desktop bridge must have:
- Immediate termination control
- Session isolation
- No credential persistence
- Operator cannot override stop

**If a kill-switch is unavailable, the bridge is prohibited.**

---

## 7. EVIDENCE & LOGGING

Each desktop authority session must record:

| Field | Required |
|-------|----------|
| Date/time | Yes |
| System accessed | Yes |
| Purpose | Yes |
| CEO confirmation | Yes |
| Artifact references | Yes |
| Outcome (success/aborted) | Yes |

**Storage location:** `/evidence/desktop/YYYY-MM-DD/`

---

## 8. FAILURE MODES & RESPONSE

| Failure | Response |
|---------|----------|
| UI change | Abort, redesign |
| MFA issue | Abort, reschedule |
| Unclear prompt | Abort |
| Unexpected terms | Abort |
| Operator error | Abort |

> **Aborting is compliance. Continuing is failure.**

---

## 9. PROHIBITED PRACTICES (ABSOLUTE)

- Unattended RPA authority actions
- Credential storage
- Screen scraping passwords
- "Just this once" exceptions
- CEO doing prep work

---

## 10. DESKTOP BRIDGE DECISION TREE

```
Is there an API?
 |-- Yes -> Use API (no desktop)
 |-- No
      |-- Is judgment required?
           |-- Yes -> Human-assisted desktop (Mode B)
           |-- No  -> Controlled RPA with kill-switch (Mode C)
```

---

## 11. CEO PROTECTION STATEMENT

```
The CEO is not a clerk.
The CEO is not a technician.
The CEO is the authority boundary.

If the system asks you to do more than approve or stop,
the system is misdesigned.
```

---

## Document Control

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-01-19 | Governance Team | Initial release |
