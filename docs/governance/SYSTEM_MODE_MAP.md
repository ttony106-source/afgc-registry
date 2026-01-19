# SYSTEM MODE MAP
## Authority-Safe Classification of External Systems

| Field | Value |
|-------|-------|
| **Document ID** | GOV-SYS-MAP-001 |
| **Version** | 1.0 |
| **Applies To** | Trust Operations, Capital Engines, Banking, Governance, Compliance |
| **Authority** | CEO / Trustee |
| **Last Reviewed** | 2026-01-19 |

---

## PURPOSE

This document pre-classifies all external systems into approved interaction modes to eliminate:
- Real-time decision-making
- Execution drift
- CEO overload

**If a system is mapped here, the decision is already made.**
**If it is not mapped here, interaction is prohibited until classified.**

---

## MODE DEFINITIONS (BINDING)

| Mode | Meaning | CEO Involvement |
|------|---------|----------------|
| **Mode A** | API-First / Fully Automatable | ❌ None |
| **Mode B** | Human-Assisted Desktop | ✅ One authority action |
| **Mode C** | Controlled RPA (Exception Only) | ✅ One authority action |
| **FORBIDDEN** | No safe authority boundary | ❌ Do not proceed |

---

## 🟢 MODE A — API-FIRST (NO CEO)

> UI use is prohibited when API access exists.

### GitHub

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | Native API, Actions, audit logs |
| **CEO Action** | None |
| **Evidence** | Git history, PRs, Actions logs |
| **Notes** | Control plane of record |

### GitHub Copilot

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | Governed by instructions + repo context |
| **CEO Action** | None |
| **Evidence** | Repo instructions, commits |

### Airtable

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | Full API, deterministic operations |
| **CEO Action** | None |
| **Evidence** | API logs, base history |

### Cloudflare

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | Stable API, infrastructure control |
| **CEO Action** | None |
| **Evidence** | API audit logs |

### Stripe

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | Payments API with strong audit trail |
| **CEO Action** | None (policy approval only, not execution) |
| **Evidence** | Stripe event logs |

### Accounting Systems (QBO / Xero)

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | API + exportable audit logs |
| **CEO Action** | None |
| **Evidence** | API sync logs |

### Email Providers (Google / M365)

| Attribute | Value |
|-----------|-------|
| **Mode** | A |
| **Why** | API-driven, no authority acceptance |
| **CEO Action** | None |
| **Evidence** | Message logs |

---

## 🟡 MODE B — HUMAN-ASSISTED DESKTOP (PREFERRED)

> Human judgment + identity required. Bots increase risk.

### Bank of America (Business / Trust Portal)

| Attribute | Value |
|-----------|-------|
| **Mode** | B |
| **Why** | MFA + legal identity binding |
| **CEO Action** | Login → review → confirm → logout |
| **Evidence** | Session log + artifact references |
| **Desktop Bridge** | Human-assisted only |

### Fidelity / Schwab / Institutional Brokers

| Attribute | Value |
|-----------|-------|
| **Mode** | B |
| **Why** | Custodial authority + variable UI |
| **CEO Action** | Single confirmation action |
| **Evidence** | Portal confirmation + evidence snapshot |

### Credit Unions / Escrow Portals

| Attribute | Value |
|-----------|-------|
| **Mode** | B |
| **Why** | Identity-bound actions |
| **CEO Action** | One authority action |
| **Evidence** | Screenshot + submission receipt |

### Government & Grant Portals

| Attribute | Value |
|-----------|-------|
| **Mode** | B |
| **Why** | Judgment + attestation required |
| **CEO Action** | Final submit / attest |
| **Evidence** | Submission receipt |

### IRS / State Tax Portals

| Attribute | Value |
|-----------|-------|
| **Mode** | B |
| **Why** | Legal declarations |
| **CEO Action** | Final confirmation only |
| **Evidence** | Filing receipt |

---

## 🟠 MODE C — CONTROLLED RPA (RARE, EXCEPTION)

> Allowed only when UI is deterministic and no judgment exists.

### Statement Downloads (Read-Only)

| Attribute | Value |
|-----------|-------|
| **Mode** | C |
| **Why** | Deterministic navigation |
| **CEO Action** | None or final confirm |
| **Controls** | Manual trigger, screen recording, kill-switch |

### File Upload Portals (No Terms / No Authority)

| Attribute | Value |
|-----------|-------|
| **Mode** | C |
| **Why** | Mechanical upload only |
| **CEO Action** | None |
| **Controls** | Stop at confirmation screen |

---

## 🔴 FORBIDDEN SYSTEMS (NO BRIDGE)

> These systems may NOT be automated or rushed.

### Notarization Platforms

| Attribute | Value |
|-----------|-------|
| **Mode** | FORBIDDEN |
| **Reason** | Identity + legal attestation combined |

### Dynamic "Agree & Continue" Legal Screens

| Attribute | Value |
|-----------|-------|
| **Mode** | FORBIDDEN |
| **Reason** | Authority + execution collapsed |

### Identity Verification / KYC Flows

| Attribute | Value |
|-----------|-------|
| **Mode** | FORBIDDEN |
| **Reason** | Non-delegable human presence |

### Any System Not Listed Here

| Attribute | Value |
|-----------|-------|
| **Mode** | FORBIDDEN |
| **Reason** | Unclassified |

---

## OPERATING RULES (NON-NEGOTIABLE)

1. **If a system is Mode A, UI use is a violation**
2. **If a system is Mode B, CEO performs only one action**
3. **Mode C requires explicit justification**
4. **Unlisted systems are forbidden by default**
5. **Deviations require an Authority PR**

---

## CEO PROTECTION STATEMENT

```
The CEO does not decide interaction modes in real time.
The system decides.
The CEO approves or stops.
```

---

## CHANGE CONTROL

Updates require:
- Authority PR (touching `/authority/` or `/board/`)
- CEO approval
- Evidence entry
- Reviewed quarterly or upon material change

---

## Document Control

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-01-19 | Governance Team | Initial classification |

---

**Once merged, this file becomes binding operating law.**
