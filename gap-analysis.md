# Gap analysis

The emulation run measured **4/8 = 50%** coverage. All four gaps are Plan B
host-level techniques (T1033, T1082, T1016, T1059.001). This is exactly the blind
spot I expected — my detections were built for AD/identity and web attacks, not
endpoint process activity — but running the emulation turned "I think I'm blind here"
into "I proved I'm blind here, and here's the fix."

## The gaps

| ID | Technique | Why it slipped through |
|----|-----------|------------------------|
| T1033 | System Owner/User Discovery | No rule keys on process creation; `whoami.exe` runs unremarked. |
| T1082 | System Information Discovery | Same — `systeminfo.exe` isn't matched by any rule. |
| T1016 | System Network Config Discovery | Same — `ipconfig /all`, `arp -a` unremarked. |
| T1059.001 | PowerShell (encoded) | Encoded PowerShell is the highest-value of the four — it's how real malware hides its command — and nothing flagged it. |

## The finding underneath the finding: a telemetry-collection gap

When I checked *why* nothing fired, I found two layers:

1. **No detection rule** for process creation (the obvious gap).
2. **The telemetry wasn't even being surfaced.** WS01 runs Sysmon and forwards to
   Wazuh, but during the run the agent was shipping the Windows **Security** channel
   while Sysmon **process-creation (Event ID 1)** events weren't coming through as
   analysable events. So even a perfect rule would have had nothing to match.

That second layer is the more important lesson: **you can't detect what you don't
collect.** A coverage gap isn't always a missing rule — sometimes it's a missing log
source. Emulation surfaced both.

### Fixing the collection gap
Ensure the WS01 Wazuh agent subscribes to the Sysmon channel in `ossec.conf`:

```xml
<localfile>
  <location>Microsoft-Windows-Sysmon/Operational</location>
  <log_format>eventchannel</log_format>
</localfile>
```

Restart the agent; confirm Sysmon Event ID 1 events appear on the manager. Only then
can a process-creation rule fire.

## Closing the highest-value gap: encoded PowerShell (T1059.001)

I picked encoded PowerShell to close first — it's the one an attacker actually relies
on, and the other three (whoami/systeminfo/ipconfig) are noisy to alert on directly.

- **New Sigma rule:** [`detections/encoded_powershell.yml`](detections/encoded_powershell.yml)
  — matches `powershell.exe`/`pwsh.exe` launched with `-EncodedCommand` / `-enc` / `-e`.
- **New Wazuh rule:** [`detections/local_rules_100016.xml`](detections/local_rules_100016.xml)
  — rule `100016`, keyed on Sysmon Event ID 1.
- **Validated as content:** the Sigma rule parses against the current Sigma spec and
  passes my own [sigmatest](https://github.com/manlikefelo/sigmatest) evaluator — the
  encoded-command sample fires, a benign `-File script.ps1` launch stays quiet.
- **Feeds back into the portfolio:** this rule belongs in my
  [detection-as-code](https://github.com/manlikefelo/detection-as-code) pipeline with a
  TP/benign test pair, and extends the coverage matrix in
  [detection-engineering](https://github.com/manlikefelo/detection-engineering).

## Re-validation status
The rule is written and validated as *content*. Live re-validation (fire it end-to-end
on WS01) is gated on the collection fix above — booting WS01 + WAZUH01, subscribing the
Sysmon channel, re-running the encoded-PowerShell atomic, and confirming rule 100016
fires. That closes the loop: **measure → find gap → collect + detect → re-measure.**

## The honest headline
Emulating a real playbook against my own lab didn't just confirm what I detect — it
found what I *don't*, including a log source I wasn't even collecting. That measure-and-
improve loop is the whole point of adversary emulation, and it's more valuable than a
coverage number that's all green.
