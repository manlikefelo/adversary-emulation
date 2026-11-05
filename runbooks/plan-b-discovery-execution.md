# Runbook: Plan B: local discovery & execution (T1033, T1082, T1016, T1059.001)

**Plan:** B · **Tactic:** Discovery / Execution · **Target:** WS01 (local)
**Detection expected:** none with the current rule set. These are the blind spots.

All four rely on **Sysmon Event ID 1 (process creation)** telemetry, which WS01 ships to
Wazuh. My current rules key on Windows Security events (4768/4769/4662) and web logs, so
they don't look at process creation, which is exactly why Plan B finds gaps.

## Atomic tests
```powershell
Invoke-AtomicTest T1033        -TestNumbers 1   # whoami
Invoke-AtomicTest T1082        -TestNumbers 1   # systeminfo
Invoke-AtomicTest T1016        -TestNumbers 1   # ipconfig /all, arp -a
Invoke-AtomicTest T1059.001    -TestNumbers 1   # powershell encoded command
```

## Expected telemetry
- **Sysmon Event ID 1** on WS01 for each spawned process: `whoami.exe`, `systeminfo.exe`,
  `ipconfig.exe`, and `powershell.exe -EncodedCommand …`.

## Expected detection
- **None** initially. After the gap analysis I add a Sigma rule for the highest-value one
  (encoded PowerShell, T1059.001) and re-run to confirm it fires. See
  [`../gap-analysis.md`](../gap-analysis.md) and [`../detections/`](../detections/).

## Result
Record each in [`../results.yml`](../results.yml): `executed: true`, `detected: false`
(then flip T1059.001 to `true` after the new rule is deployed and re-validated).
