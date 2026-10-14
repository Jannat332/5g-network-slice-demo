"""Automated unit test suite for 5G network slicing simulator."""

import unittest
from src.packet import Packet, SliceType, QOS_PROFILES
from src.scheduler import FIFOScheduler, SlicedPriorityScheduler
from src.simulator import run_simulation


class TestSchedulers(unittest.TestCase):

    def test_fifo_ordering(self):
        fifo = FIFOScheduler()
        p1 = Packet(1, SliceType.EMBB, 1400, 0.0)
        p2 = Packet(2, SliceType.URLLC, 64, 1.0)
        fifo.enqueue(p1)
        fifo.enqueue(p2)

        # In FIFO, p1 must come out first regardless of slice priority
        self.assertEqual(fifo.dequeue().packet_id, 1)
        self.assertEqual(fifo.dequeue().packet_id, 2)
        self.assertTrue(fifo.is_empty())

    def test_sliced_priority_preemption(self):
        sliced = SlicedPriorityScheduler()
        p1 = Packet(1, SliceType.EMBB, 1400, 0.0)
        p2 = Packet(2, SliceType.URLLC, 64, 1.0)
        sliced.enqueue(p1)
        sliced.enqueue(p2)

        # In Sliced, URLLC packet p2 must be dequeued before eMBB packet p1
        first_out = sliced.dequeue()
        self.assertEqual(first_out.slice_type, SliceType.URLLC)
        self.assertEqual(first_out.packet_id, 2)

        second_out = sliced.dequeue()
        self.assertEqual(second_out.slice_type, SliceType.EMBB)
        self.assertEqual(second_out.packet_id, 1)
        self.assertTrue(sliced.is_empty())


class TestSimulationDynamics(unittest.TestCase):

    def test_slicing_eliminates_urllc_sla_violations(self):
        fifo_stats = run_simulation("FIFO", bandwidth_mbps=8.0, duration_ms=500.0, seed=123)
        sliced_stats = run_simulation("SLICED", bandwidth_mbps=8.0, duration_ms=500.0, seed=123)

        # Both modes deliver packets
        self.assertGreater(fifo_stats.urllc_delivered, 0)
        self.assertGreater(sliced_stats.urllc_delivered, 0)

        # Sliced mode should have significantly lower URLLC average latency
        self.assertLess(sliced_stats.urllc_avg_latency_ms, fifo_stats.urllc_avg_latency_ms)

        # Sliced mode must maintain URLLC p99 under 3GPP PDB (10ms)
        self.assertLessEqual(sliced_stats.urllc_p99_latency_ms, QOS_PROFILES[SliceType.URLLC].pdb_ms)


if __name__ == "__main__":
    unittest.main()
