# System Architecture - 5G Network Slice QoS Simulator

## Overview
`5g-network-slice-demo` models 3GPP Release 16/17 network slicing mechanisms. It simulates how a physical RAN/UPF transport bottleneck dynamically prioritizes Ultra-Reliable Low-Latency Communication (URLLC) over Enhanced Mobile Broadband (eMBB) traffic under heavy link congestion.

## Architecture Diagram

```
 [URLLC Traffic Generator]                [eMBB Traffic Generator]
  - 5QI 82 (Robotics/Safety)               - 5QI 9 (4K Video/Data)
  - Small packets (128B)                   - Jumbo frames (1500B)
  - Strict PDB <= 10ms                     - Best-effort PDB 300ms
             |                                        |
             +-------------------+--------------------+
                                 |
                                 v
             +----------------------------------------+
             |         5G Slice Scheduler / UPF       |
             |                                        |
             |  +----------------+  +---------------+ |
             |  | Priority Queue |  | Deficit Round | |
             |  |    (URLLC)     |  |  Robin (eMBB) | |
             |  +----------------+  +---------------+ |
             +----------------------------------------+
                                 |
                                 v (Constrained Bandwidth Link)
             +----------------------------------------+
             |       SLA & QoS Analytics Engine       |
             |  - Latency (p50, p95, p99)             |
             |  - Jitter Calculation                  |
             |  - 3GPP 5QI SLA Violation Monitor      |
             +----------------------------------------+
```

## Core Modules
1. **Packet Models (`packet.py`)**: Defines 3GPP packet headers, 5QI tags, Slice Identifiers (S-NSSAI: SST=1 for eMBB, SST=2 for URLLC), arrival timestamps, and packet payload sizes.
2. **Slice Scheduler (`scheduler.py`)**: Implements strict-priority preemption with token bucket rate limiting for the shared transport pipe.
3. **Analytics Engine (`metrics.py`)**: Computes Packet Delay Budgets (PDB), Jitter, packet drops, and SLA breach percentages.
