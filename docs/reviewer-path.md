# Reviewer path: a 3-minute guided tour

For a hiring manager or teammate. This repo runs ATT&CK techniques against my lab and
**measures** which detections fire, purple-team validation, not just attacking.

### 1 · The coverage layer first (60s)  →  `reports/`
Open [`reports/coverage-report.md`](../reports/coverage-report.md): **4/8 techniques
detected = 50%**, one row per technique with detected yes/no and the rule that caught it.
[`reports/navigator-layer.json`](../reports/navigator-layer.json) is the same data as an
ATT&CK Navigator heat-map (green = detected, red = gap), load it at
mitre-attack.github.io/attack-navigator. That coloured grid is the headline: it says "I
measure coverage" faster than any paragraph.

### 2 · One runbook (30s)  →  `runbooks/T1558.003-kerberoasting.md`
[A runbook](../runbooks/T1558.003-kerberoasting.md) shows the discipline per technique:
the exact Atomic test, the telemetry it should produce, and which of my rules *should*
catch it. This is how the coverage number is derived, technique by technique.

### 3 · The gap analysis (90s)  →  `gap-analysis.md`
[`gap-analysis.md`](../gap-analysis.md) is the most important file. The emulation found a
real blind spot, endpoint process activity, and, digging in, a **telemetry-collection
gap**: I wasn't even collecting the Sysmon process-creation events a rule would need.
I closed the highest-value gap (encoded PowerShell, T1059.001) with a new Sigma + Wazuh
rule, validated against the Sigma spec and my own [sigmatest](https://github.com/manlikefelo/sigmatest)
tool. [`RUN-LOG.md`](../RUN-LOG.md) records the live run step by step.

---
**The takeaway:** I don't just claim coverage: I emulate a real playbook, measure it,
and find (and fix) my own gaps, including a log source I wasn't collecting. That
measure-and-improve loop is exactly what adversary emulation is for.
