# Emulation Plan A — AD credential access & domain dominance

**Objective:** emulate the credential-theft path an intrusion actor takes once it has a
foothold in an Active Directory network, and measure which steps my existing detections
catch. This plan deliberately mirrors the TTPs of financially-motivated and
espionage actors who lean on Kerberos abuse and DCSync — e.g. **Wizard Spider / FIN6-style**
tradecraft, where roasting a service account and then replicating secrets from the DC is
the standard route to Domain Admin.

**Scope:** my own isolated lab only (`lab.local`, host-only `10.10.10.0/24`). Every
technique is run with Atomic Red Team on WS01 (domain-joined workstation) against DC01.

## The chain (ATT&CK)

```
Discovery              Credential Access                 Cred Access (impact)
──────────             ─────────────────                 ────────────────────
T1087.002  ──────────► T1558.003 Kerberoasting  ───────► T1003.006 DCSync
Account Discovery      (roast svc_sql SPN)               (replicate krbtgt +
(BloodHound/           T1558.004 AS-REP Roasting          all domain hashes)
 LDAP recon)           (roast b.otieno)
```

## Techniques in scope

| # | Technique | ID | Atomic(s) | Detection expected |
|---|-----------|----|-----------|--------------------|
| A1 | Account/Group Discovery (domain) | T1087.002 | ART T1087.002 (net group /domain, PowerView) | rule 100013 (read burst) |
| A2 | Kerberoasting | T1558.003 | ART T1558.003 (Rubeus/PowerView TGS request) | rule 100010 (4769 RC4) |
| A3 | AS-REP Roasting | T1558.004 | ART T1558.004 (Rubeus asreproast) | rule 100011 (4768 preauth 0) |
| A4 | DCSync | T1003.006 | ART T1003.006 (mimikatz lsadump::dcsync) | rule 100012 (4662 replication GUID) |

## Success criteria
- Each technique executes cleanly and produces the expected telemetry on WS01/DC01.
- For each, I record whether the mapped Wazuh rule fired (→ `results.yml`).
- Any technique that runs but does **not** alert is logged as a gap for Plan-level
  follow-up (see [`../gap-analysis.md`](../gap-analysis.md)).

## Why this plan
It re-attacks the same lab as my [ad-attack-chain](https://github.com/manlikefelo/ad-attack-chain)
project, but *systematically* and through a recognised emulation framework, so the
result is a measured coverage figure rather than "I ran some attacks." It validates the
detections from [detection-engineering](https://github.com/manlikefelo/detection-engineering) /
[detection-as-code](https://github.com/manlikefelo/detection-as-code).
