# Run log: adversary emulation session (2026-08-05)

A record of the live emulation run, paced one step at a time against the isolated lab.

## Environment
- Host: 16GB RAM, VirtualBox. Ran **WAZUH01 (8GB) + WS01 (4GB)** this phase; **DC01
  was kept powered off** to stay within the RAM budget (see the lab's low-RAM operating
  guide: DC01+WS01+WAZUH01 together thrash the box).
- WS01 (`10.10.10.20`) domain-joined to `lab.local`, Sysmon + Wazuh agent running.
- Driven from the host with `VBoxManage guestcontrol` (copy a .ps1 in, run it, copy
  results out: the reliable pattern under memory pressure).

## What I verified
1. **Telemetry pipeline healthy:** WS01 Wazuh agent (id 002) **Active** on the manager;
   464 WS01 events archived during the run, events are flowing agent → manager.
2. **Plan B executed live on WS01** (T1033 whoami, T1082 systeminfo, T1016 ipconfig/arp,
   T1059.001 encoded PowerShell). Completion markers confirmed.
3. **Plan B produced zero detections**: the gap this project set out to find. (A lone
   regex hit on "arp" was DNS rule 61109 for `in-addr.arpa`, unrelated; discounted.)
4. **A second-layer finding:** WS01's agent is forwarding the Windows **Security**
   channel, but Sysmon **process-creation (EID 1)** events are not being surfaced, so
   under the missing detection rule there's also a **telemetry-collection** gap. Both are
   written up in [`gap-analysis.md`](gap-analysis.md).

## Plan A (AD techniques)
Kerberoasting / AS-REP / DCSync / domain discovery were **verified firing end-to-end in
my [ad-attack-chain](https://github.com/manlikefelo/ad-attack-chain) project** (rules
100010–100013, evidence in that repo). They need DC01 live, which the RAM budget didn't
allow alongside WS01+WAZUH01 this session, so I record them in `results.yml` with
`source: ad-attack-chain` rather than claiming a fresh run here: the coverage figure
stays honest.

## Coverage result
**4/8 executed techniques detected = 50%** (see [`reports/coverage-report.md`](reports/coverage-report.md)
and the Navigator layer). The four gaps are all Plan B host-level techniques, exactly
the blind spot the plan predicted, and drive the gap analysis + new rule 100016.

## Cleanup
- Reverted the temporary `logall_json` change on the Wazuh manager (set for evidence
  capture) back to its default.
- Removed `C:\lab` scratch dir on WS01.
- Powered all VMs off; host RAM released.
