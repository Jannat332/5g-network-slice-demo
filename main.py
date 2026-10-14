#!/usr/bin/env python3
"""CLI Entrypoint for 5G Network Slicing QoS Simulator."""

import argparse
from src.simulator import run_simulation
from src.visualizer import render_comparison_table


def main():
    parser = argparse.ArgumentParser(
        description="Simulates 3GPP 5G Network Slicing (URLLC vs eMBB) under congestion."
    )
    parser.add_argument(
        "--bandwidth", "-b",
        type=float,
        default=10.0,
        help="Shared transport link bandwidth in Mbps (default: 10.0 Mbps)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=float,
        default=1000.0,
        help="Simulation run duration in milliseconds (default: 1000 ms)"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=42,
        help="Random seed for deterministic traffic generation (default: 42)"
    )

    args = parser.parse_args()

    print("\nRunning legacy unsliced FIFO transmission simulation...")
    fifo_stats = run_simulation("FIFO", bandwidth_mbps=args.bandwidth, duration_ms=args.duration, seed=args.seed)

    print("Running 3GPP 5G Sliced priority transmission simulation...\n")
    sliced_stats = run_simulation("SLICED", bandwidth_mbps=args.bandwidth, duration_ms=args.duration, seed=args.seed)

    print(render_comparison_table(fifo_stats, sliced_stats))


if __name__ == "__main__":
    main()
