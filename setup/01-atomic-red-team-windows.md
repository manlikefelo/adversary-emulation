# Setup: Atomic Red Team (Invoke-Atomic) on WS01

> ## SAFETY, read first
> Atomic Red Team executes **real** offensive techniques. Run it **only** against
> systems you own, in an **isolated** environment. This lab is a host-only network
> (`10.10.10.0/24`) with **no route to the internet or any production system**, on VMs
> I can snapshot and roll back. Never run these atomics on a machine you rely on, a
> corporate device, or anything reachable from a real network. Snapshot the VM before
> a run so you can revert.

## Target
WS01: the domain-joined Windows 11 workstation (`10.10.10.20`), which already ships
**Sysmon + Windows Security** telemetry to the Wazuh manager. That existing visibility is
needed because I attack WS01/DC01 and watch which of my detections fire on WAZUH01.

## Install Invoke-Atomic (PowerShell, elevated)

```powershell
# Allow the install for this session only
Set-ExecutionPolicy Bypass -Scope Process -Force

# Install the Invoke-AtomicRedTeam module + the atomics folder
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics -Force

# Load it
Import-Module "C:\AtomicRedTeam\invoke-atomicredteam\Invoke-AtomicRedTeam.psd1" -Force
```

> **Offline lab note:** WS01 is host-only and can't reach GitHub. Two options:
> 1. Temporarily attach WS01's NAT NIC for the one-time install, then detach it before
>    running atomics (keeps the attack phase fully isolated); **or**
> 2. Download the `invoke-atomicredteam` + `atomic-red-team` zips on the host and copy
>    them into the guest with `VBoxManage guestcontrol copyto`, then point
>    `$PSAtomicRedTeamPath` at the extracted folder. This is the safer option and the one
>    I used: the attack phase never has a route off the lab.

## Verify

```powershell
Invoke-AtomicTest T1033 -ShowDetails      # should list the whoami atomic
```

## Running a test (pattern)

```powershell
Invoke-AtomicTest T1558.003 -TestNumbers 1 -GetPrereqs   # stage prerequisites
Invoke-AtomicTest T1558.003 -TestNumbers 1               # execute
Invoke-AtomicTest T1558.003 -TestNumbers 1 -Cleanup      # revert changes
```

Run **one technique at a time**, read the telemetry it produces in Wazuh before moving
on, and record the result. See the [runbooks](../runbooks/) for each technique's exact
test, expected telemetry, and mapped detection rule.

## Driving WS01 headless
This lab is driven from the host with `VBoxManage guestcontrol` (Guest Additions is
installed), copying a `.ps1` into the guest and running it: the same pattern used
across the portfolio. Credentials are never stored in this repo.
