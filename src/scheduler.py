"""5G Slice and FIFO Transport Schedulers."""

from collections import deque
from typing import List, Optional
from src.packet import Packet, SliceType


class FIFOScheduler:
    """Legacy un-sliced scheduler: all packets enter a single FIFO queue."""

    def __init__(self):
        self.queue = deque()

    def enqueue(self, packet: Packet):
        self.queue.append(packet)

    def dequeue(self) -> Optional[Packet]:
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def queue_size(self) -> int:
        return len(self.queue)


class SlicedPriorityScheduler:
    """3GPP 5G Sliced Scheduler: Dedicated queues with URLLC strict priority preemption."""

    def __init__(self):
        self.urllc_queue = deque()
        self.embb_queue = deque()

    def enqueue(self, packet: Packet):
        if packet.slice_type == SliceType.URLLC:
            self.urllc_queue.append(packet)
        else:
            self.embb_queue.append(packet)

    def dequeue(self) -> Optional[Packet]:
        # Strict priority: Serve all pending URLLC packets first
        if self.urllc_queue:
            return self.urllc_queue.popleft()
        elif self.embb_queue:
            return self.embb_queue.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self.urllc_queue) == 0 and len(self.embb_queue) == 0

    def queue_size(self) -> int:
        return len(self.urllc_queue) + len(self.embb_queue)
