# Emulation Plan B: local discovery & execution (finding my blind spots)

**Objective:** deliberately run common **host-level** discovery and execution techniques
that my current detections were *not* written for, so the coverage report shows honest
gaps and I have real material for the gap analysis. My detections so far are AD/identity-
and web-centric; a real intrusion also generates a lot of noisy-but-important
host telemetry, and I want to see what I'm blind to.

**Scope:** my own isolated lab only, run with Atomic Red Team on WS01.

**Threat model:** this mirrors the "land and look around" phase every actor performs
right after initial access: the `whoami`, `systeminfo`, `net` and script-execution
activity that shows up in Sysmon before the flashier credential attacks. Emulating it
tests whether I have any process-level visibility, not just event-log signatures.

## Techniques in scope

| # | Technique | ID | Atomic(s) | Detection expected |
|---|-----------|----|-----------|--------------------|
| B1 | System Owner/User Discovery | T1033 | ART T1033 (whoami) | **none yet, likely gap** |
| B2 | System Information Discovery | T1082 | ART T1082 (systeminfo) | **none yet, likely gap** |
| B3 | System Network Config Discovery | T1016 | ART T1016 (ipconfig /all, arp -a) | **none yet, likely gap** |
| B4 | Command & Scripting: PowerShell | T1059.001 | ART T1059.001 (encoded command) | **none yet, likely gap** |

## Expectation
I expect most of Plan B to be **undetected** with my current rule set. That's the point.
Plan B exists to prove I can find and close blind spots, not to pad the coverage number.
I'll pick 2–3 of these gaps and write new Sigma detections against the Sysmon telemetry
they produce (Event ID 1 process creation), then re-run to confirm the new rules fire.

## Success criteria
- Each technique executes and produces Sysmon process-creation telemetry on WS01.
- Coverage report shows them as executed→undetected (red on the Navigator layer).
- At least 2 are closed with new detections in [`../gap-analysis.md`](../gap-analysis.md)
  and [`../detections/`](../detections/), then re-validated.
