# Project Workflow & Requirements (PWD) - 5G Network Slice Simulator

## 1. Problem Statement
In industrial private 5G networks (e.g. smart factories, automated mining, autonomous ports in Finland), time-critical machine telemetry and automated guided vehicles (AGVs) must operate on the same physical wireless infrastructure as high-definition surveillance video and office internet. Without slicing, bulk video traffic causes bufferbloat, delaying critical stop signals and causing industrial hazards.

## 2. Functional Requirements
- **FR-1 Dual-Slice Traffic Generation**:
  - **URLLC Slice**: High frequency, small payloads (128 bytes), strict 10ms Packet Delay Budget.
  - **eMBB Slice**: High throughput, large payloads (1400 bytes), flexible 300ms delay tolerance.
- **FR-2 Congestion Simulation**:
  - Dynamically ramp traffic load from 50% capacity up to 160% capacity to induce severe packet queueing.
- **FR-3 Dual Scheduling Modes**:
  - **Mode A (Un-sliced / FIFO)**: Single shared queue with First-In First-Out service.
  - **Mode B (5G Sliced / Priority)**: Dedicated URLLC priority queue bypassing bulk eMBB buffers.
- **FR-4 Comparative SLA Metrics**:
  - Output side-by-side comparison of Average Latency, p99 Latency, and SLA Breach Count between sliced vs unsliced modes.

## 3. Non-Functional Requirements
- **Standards Adherence**: Conform to 3GPP TS 23.501 (System Architecture for 5G) QoS parameters (5QI, PDB).
- **Zero Heavy Setup**: Runs entirely in Python standard library without requiring complex 20GB Open5GS/SDR hardware.
