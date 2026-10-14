# 5G Network Slice QoS Simulator (3GPP URLLC vs eMBB)

A discrete-event simulation engine modeling **3GPP Release 16/17 5G Network Slicing**. It demonstrates how priority scheduling and slice isolation protect delay-critical industrial control packets (URLLC) from bufferbloat during heavy broadband traffic (eMBB) congestion.

---

## 3GPP QoS Mapping & Problem Context
In automated factories, ports, and robotic machinery, safety commands require **Ultra-Reliable Low-Latency Communication (URLLC)**. If these packets share an un-sliced transport pipe with bulk 4K video surveillance (**eMBB**), bulk packets cause catastrophic queueing delays.

| Slice Name | 3GPP SST | 5QI Index | Packet Delay Budget (PDB) | Application Example |
|---|---|---|---|---|
| **URLLC** | SST 2 | 82 | **<= 10 ms** | Emergency Braking, Robotics, Sensor Telemetry |
| **eMBB**  | SST 1 | 9  | **<= 300 ms** | 4K Camera Feeds, Bulk Diagnostics, File Transfers |

---

## Benchmark Results (10 Mbps Bottleneck Link)

```
==============================================================================
  3GPP 5G NETWORK SLICING QoS PERFORMANCE BENCHMARK
  Bottleneck Link: 10 Mbps  |  Duration: 1000 ms  |  Congestion: High
==============================================================================
Metric                             | Legacy Unsliced (FIFO) | 5G Sliced (Priority)
------------------------------------------------------------------------------
URLLC Delivered Packets            | 200                | 200               
URLLC Average Latency              | 109.85 ms          | 0.68 ms           
URLLC 99th Percentile (p99)        | 237.93 ms          | 1.25 ms           
URLLC Peak Latency                 | 238.33 ms          | 1.25 ms           
URLLC SLA Violations (>10ms)       | 195 (CRITICAL)     | 0 (PASSED)        
------------------------------------------------------------------------------
eMBB Delivered Packets             | 1085               | 1085              
eMBB Average Latency               | 113.36 ms          | 115.19 ms         
eMBB SLA Violations (>300ms)       | 0                  | 0                 
==============================================================================
```

---

## Project Structure
```
05-5g-network-slice-demo/
├── src/
│   ├── packet.py        # 3GPP 5QI packet models and SLA definitions
│   ├── scheduler.py     # FIFO and Sliced priority queue implementations
│   ├── simulator.py     # Discrete-event transmission serialization loop
│   └── visualizer.py    # Terminal comparative benchmarking table
├── tests/
│   └── test_simulation.py # Automated test suite (Python unittest)
├── main.py              # CLI entrypoint with configurable bandwidth & duration
├── arch.md              # 3GPP RAN/UPF slice architecture diagram
├── pwd.md               # Product requirements & workflow documentation
├── design.md            # Mathematical queue formulas & 5QI tables
├── memory.md            # Architectural decisions and tradeoffs
├── rules.md             # Telecom standards and coding guidelines
└── bug-report.md        # Testing logs & resolved edge cases
```

---

## Quickstart

### Prerequisites
- Python 3.9+ (Zero third-party dependencies required; runs entirely with the Python standard library!)

### Running the Benchmark
```bash
# Run default simulation (10 Mbps link, 1000 ms)
python main.py

# Test with higher bandwidth or longer duration
python main.py --bandwidth 20.0 --duration 2000

# Test with extreme bottleneck (5 Mbps link)
python main.py --bandwidth 5.0
```

### Running Unit Tests
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## License
MIT License.
