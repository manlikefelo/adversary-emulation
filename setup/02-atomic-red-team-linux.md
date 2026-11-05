# Setup: Atomic Red Team on a Linux host (UB01)

> Same safety rules as the Windows guide, isolated lab only, snapshot first.

Atomic Red Team also covers Linux techniques. UB01 (`10.10.10.30`, Ubuntu + Docker,
already running the vulnerable containers from my web-pentest project) is the Linux target.

## Install (Invoke-Atomic via PowerShell Core, or run atomics manually)

Atomic Red Team's canonical runner is PowerShell, so install PowerShell 7 on UB01:

```bash
# Ubuntu 22.04
sudo apt-get update && sudo apt-get install -y wget apt-transport-https software-properties-common
wget -q https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb && sudo apt-get update
sudo apt-get install -y powershell
```

```powershell
pwsh
IEX (IWR 'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1' -UseBasicParsing)
Install-AtomicRedTeam -getAtomics -Force
Import-Module Invoke-AtomicRedTeam -Force
```

Alternatively, many Linux atomics are plain shell one-liners you can copy from the
`atomics/<technique>/T####.yaml` files and run directly, which avoids installing pwsh.

## Scope for this project
The lab's detections and emulation focus on the **Windows/AD** side (WS01/DC01), where my
rule set lives. UB01 is documented here for completeness and as the natural place to
extend Linux-technique emulation next; the executed Plan A/B runs target WS01/DC01.
