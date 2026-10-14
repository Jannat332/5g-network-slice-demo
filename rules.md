# Engineering Rules & Guidelines - 5G Network Slice Simulator

## 1. Principles
- **KISS**: Use Python's built-in `collections.deque` and random generators to model queue dynamics. Avoid heavyweight third-party discrete-event simulation frameworks like SimPy unless complex radio channel fading is modeled.
- **DRY**: Both FIFO and Sliced schedulers inherit or share packet departure and metric collection pipelines (`record_packet_departure`).

## 2. Telecom Standards Alignment
- Always reference the 3GPP Technical Specification (TS 23.501 Clause 5.7) for QoS attributes.
- Ensure that URLLC packet sizes reflect real sensor/machine commands (typically 64 - 256 bytes) rather than artificial giant payloads.
- Latency calculations must distinguish between transmission time (bandwidth-dependent) and queue waiting delay (bufferbloat-dependent).
