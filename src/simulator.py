"""Discrete-event simulation engine for 5G network slicing."""

import random
from dataclasses import dataclass
from typing import List, Tuple
from src.packet import Packet, SliceType, QOS_PROFILES
from src.scheduler import FIFOScheduler, SlicedPriorityScheduler


@dataclass
class SimulationStats:
    mode_name: str
    urllc_delivered: int
    urllc_avg_latency_ms: float
    urllc_p99_latency_ms: float
    urllc_max_latency_ms: float
    urllc_sla_violations: int
    embb_delivered: int
    embb_avg_latency_ms: float
    embb_p99_latency_ms: float
    embb_max_latency_ms: float
    embb_sla_violations: int


def generate_traffic_stream(duration_ms: float = 1000.0, seed: int = 42) -> List[Packet]:
    """Generates synthetic inter-arrival packets for URLLC and eMBB streams."""
    random.seed(seed)
    packets = []
    packet_id = 1

    # URLLC: Periodic control messages (e.g. 1 packet every 5ms)
    t = 0.0
    while t < duration_ms:
        packets.append(Packet(
            packet_id=packet_id,
            slice_type=SliceType.URLLC,
            size_bytes=random.randint(64, 128),  # Tiny command frame
            creation_time_ms=round(t, 3)
        ))
        packet_id += 1
        t += random.uniform(3.0, 7.0)

    # eMBB: Heavy video traffic bursts (e.g. 1400 bytes, bursty inter-arrival)
    t = 0.0
    while t < duration_ms:
        # Simulate traffic burst every 100ms
        burst_size = random.randint(3, 8)
        for _ in range(burst_size):
            packets.append(Packet(
                packet_id=packet_id,
                slice_type=SliceType.EMBB,
                size_bytes=random.randint(1200, 1500),
                creation_time_ms=round(t, 3)
            ))
            packet_id += 1
        t += random.uniform(2.0, 8.0)

    # Sort deterministically by creation time
    packets.sort(key=lambda p: p.creation_time_ms)
    return packets


def run_simulation(scheduler_type: str, bandwidth_mbps: float = 10.0, duration_ms: float = 1000.0, seed: int = 42) -> SimulationStats:
    """Executes discrete transmission loop over a constrained radio link."""
    traffic = generate_traffic_stream(duration_ms=duration_ms, seed=seed)

    scheduler = FIFOScheduler() if scheduler_type == "FIFO" else SlicedPriorityScheduler()

    # Link speed in bytes per millisecond: (mbps * 1_000_000) / (8 * 1000)
    bytes_per_ms = (bandwidth_mbps * 125.0)

    current_time_ms = 0.0
    traffic_idx = 0
    total_packets = len(traffic)
    delivered_packets: List[Packet] = []

    active_tx_remaining_bytes = 0.0
    active_packet: Packet = None

    time_step_ms = 0.1  # 100 microsecond time slice

    while current_time_ms <= duration_ms or not scheduler.is_empty() or active_packet is not None:
        # Enqueue new arrivals
        while traffic_idx < total_packets and traffic[traffic_idx].creation_time_ms <= current_time_ms:
            scheduler.enqueue(traffic[traffic_idx])
            traffic_idx += 1

        # Service active transmission
        if active_packet is not None:
            bytes_sent = bytes_per_ms * time_step_ms
            active_tx_remaining_bytes -= bytes_sent

            if active_tx_remaining_bytes <= 0:
                active_packet.departure_time_ms = round(current_time_ms, 3)
                delivered_packets.append(active_packet)
                active_packet = None

        # Pick next packet if channel is free
        if active_packet is None and not scheduler.is_empty():
            active_packet = scheduler.dequeue()
            active_tx_remaining_bytes = active_packet.size_bytes

        current_time_ms += time_step_ms
        if current_time_ms > duration_ms + 2000.0:
            # Safety timeout to avoid infinite loops on extreme saturation
            break

    # Calculate metrics
    urllc_pkts = [p for p in delivered_packets if p.slice_type == SliceType.URLLC]
    embb_pkts = [p for p in delivered_packets if p.slice_type == SliceType.EMBB]

    def stats_for(pkts: List[Packet], default_pdb: float):
        if not pkts:
            return 0, 0.0, 0.0, 0.0, 0
        latencies = sorted([p.latency_ms for p in pkts])
        avg_lat = round(sum(latencies) / len(latencies), 2)
        p99_idx = int(len(latencies) * 0.99)
        p99_lat = round(latencies[min(p99_idx, len(latencies) - 1)], 2)
        max_lat = round(latencies[-1], 2)
        violations = sum(1 for p in pkts if p.latency_ms > default_pdb)
        return len(pkts), avg_lat, p99_lat, max_lat, violations

    u_count, u_avg, u_p99, u_max, u_viol = stats_for(urllc_pkts, QOS_PROFILES[SliceType.URLLC].pdb_ms)
    e_count, e_avg, e_p99, e_max, e_viol = stats_for(embb_pkts, QOS_PROFILES[SliceType.EMBB].pdb_ms)

    return SimulationStats(
        mode_name=scheduler_type,
        urllc_delivered=u_count,
        urllc_avg_latency_ms=u_avg,
        urllc_p99_latency_ms=u_p99,
        urllc_max_latency_ms=u_max,
        urllc_sla_violations=u_viol,
        embb_delivered=e_count,
        embb_avg_latency_ms=e_avg,
        embb_p99_latency_ms=e_p99,
        embb_max_latency_ms=e_max,
        embb_sla_violations=e_viol
    )
