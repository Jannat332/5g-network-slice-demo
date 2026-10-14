# Software Design Specification - 5G Network Slice Simulator

## 3GPP 5G QoS Identifier (5QI) Mapping
| Slice | Slice Type (SST) | 5QI | Resource Type | Packet Delay Budget (PDB) | Packet Error Rate |
|---|---|---|---|---|---|
| **eMBB** | SST 1 | 9 | Non-GBR | 300 ms | $10^{-6}$ |
| **URLLC** | SST 2 | 82 | Delay-Critical GBR | 10 ms | $10^{-5}$ |

## Data Models
```python
from dataclasses import dataclass
from enum import Enum

class SliceType(Enum):
    EMBB = "eMBB"
    URLLC = "URLLC"

@dataclass
class Packet:
    packet_id: int
    slice_type: SliceType
    size_bytes: int
    creation_time_ms: float
    service_time_ms: float = 0.0
    queue_delay_ms: float = 0.0

@dataclass
class SliceMetrics:
    slice_type: SliceType
    packets_sent: int
    packets_delivered: int
    avg_latency_ms: float
    p99_latency_ms: float
    max_latency_ms: float
    sla_violations: int
```

## Scheduling Algorithms
1. **FIFO (Legacy / Unsliced)**:
   $$\text{Queue} = [P_1, P_2, \dots, P_n] \implies \text{Latency}(P_{URLLC}) = \sum \text{TransmissionTime}(P_{eMBB})$$
2. **5G Priority Slicing**:
   $$\text{Serve } P \in \text{Queue}_{URLLC} \text{ if } \text{len}(\text{Queue}_{URLLC}) > 0 \text{ else } \text{Queue}_{eMBB}$$
