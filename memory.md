# Memory & Decision Log - 5G Network Slice Simulator

## Context & Key Decisions
- **Decision 1: Discrete-Event Queuing Model over Heavy SDR Software**
  - *Rationale*: Running real 5G testbeds like Open5GS + UERANSIM requires 16GB of RAM, Linux kernel modules (`gtp5g`), and root privileges that cannot be demoed in a quick 5-minute technical interview. A discrete-event queuing simulator demonstrates 3GPP QoS concepts, packet delay budgets, and buffer dynamics instantly on any laptop.
- **Decision 2: 3GPP 5QI Standard Values**
  - *Rationale*: Rather than using arbitrary numbers, using exact 3GPP TS 23.501 values (5QI 82: 10ms PDB for URLLC; 5QI 9: 300ms for eMBB) gives the project technical credibility with telecom interviewers at Nokia, Ericsson, or Aalto University.
- **Decision 3: Direct Side-by-Side Comparison Output**
  - *Rationale*: Showing both unsliced FIFO and sliced priority outputs side-by-side provides immediate visual proof of how slicing prevents URLLC SLA breaches.
