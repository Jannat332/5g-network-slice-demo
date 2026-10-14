"""3GPP Packet and QoS Profile definitions."""

from dataclasses import dataclass
from enum import Enum


class SliceType(Enum):
    EMBB = "eMBB"    # 3GPP SST 1 (Enhanced Mobile Broadband)
    URLLC = "URLLC"  # 3GPP SST 2 (Ultra-Reliable Low-Latency)


@dataclass(frozen=True)
class QoSProfile:
    slice_type: SliceType
    five_qi: int            # 3GPP 5G QoS Identifier
    pdb_ms: float           # Packet Delay Budget in milliseconds
    priority_level: int     # Lower value = higher priority in 3GPP


# 3GPP TS 23.501 standardized profiles
QOS_PROFILES = {
    SliceType.URLLC: QoSProfile(
        slice_type=SliceType.URLLC,
        five_qi=82,
        pdb_ms=10.0,
        priority_level=1
    ),
    SliceType.EMBB: QoSProfile(
        slice_type=SliceType.EMBB,
        five_qi=9,
        pdb_ms=300.0,
        priority_level=9
    )
}


@dataclass
class Packet:
    packet_id: int
    slice_type: SliceType
    size_bytes: int
    creation_time_ms: float
    departure_time_ms: float = 0.0

    @property
    def latency_ms(self) -> float:
        return max(0.0, self.departure_time_ms - self.creation_time_ms)

    @property
    def qos_profile(self) -> QoSProfile:
        return QOS_PROFILES[self.slice_type]

    @property
    def is_sla_violated(self) -> bool:
        return self.latency_ms > self.qos_profile.pdb_ms
