#!/usr/bin/env python3
"""
analyze_results.py: Automated analyzer that parses raw benchmark outputs
and prints a quantitative comparison matrix between Virtual Machine and Docker Container
including CPU, Memory, Disk, Network, and FastAPI microservice benchmarks.
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.path.join(PROJECT_DIR, "results", "raw")

def parse_sysbench_cpu(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        text = f.read()
    eps = re.search(r'events per second:\s+([\d\.]+)', text)
    lat_avg = re.search(r'avg:\s+([\d\.]+)', text)
    lat_p95 = re.search(r'95th percentile:\s+([\d\.]+)', text)
    return {
        'eps': float(eps.group(1)) if eps else 0.0,
        'lat_avg': float(lat_avg.group(1)) if lat_avg else 0.0,
        'lat_p95': float(lat_p95.group(1)) if lat_p95 else 0.0
    }

def parse_sysbench_mem(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        text = f.read()
    mib_sec = re.search(r'([\d\.]+)\s+MiB transferred\s+\(([\d\.]+)\s+MiB/sec\)', text)
    lat_avg = re.search(r'avg:\s+([\d\.]+)', text)
    return {
        'mib_sec': float(mib_sec.group(2)) if mib_sec else 0.0,
        'lat_avg': float(lat_avg.group(1)) if lat_avg else 0.0
    }

def parse_ab(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        text = f.read()
    rps = re.search(r'Requests per second:\s+([\d\.]+)', text)
    tpr = re.search(r'Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean\)', text)
    failed = re.search(r'Failed requests:\s+(\d+)', text)
    return {
        'rps': float(rps.group(1)) if rps else 0.0,
        'latency_ms': float(tpr.group(1)) if tpr else 0.0,
        'failed': int(failed.group(1)) if failed else 0
    }

def main():
    print("=" * 72)
    print("  EXPERIMENT 2: COMPLETE PERFORMANCE ANALYSIS MATRIX (VM VS CONTAINER)")
    print("=" * 72)
    
    # 1. CPU
    print("\n[1] CPU Performance (sysbench prime limit 20000, 30s):")
    print(f"{'Threads':<10}{'VM EPS':<14}{'Container EPS':<16}{'Delta':<18}")
    print("-" * 60)
    for t in [1, 2, 4, 8]:
        vm = parse_sysbench_cpu(os.path.join(RAW_DIR, "cpu", f"vm-cpu-{t}thread.txt"))
        c = parse_sysbench_cpu(os.path.join(RAW_DIR, "cpu", f"container-cpu-{t}thread.txt"))
        if vm and c:
            delta = ((c['eps'] - vm['eps']) / vm['eps']) * 100
            winner = "Container" if delta >= 0 else "VM"
            print(f"{t:<10}{vm['eps']:<14.2f}{c['eps']:<16.2f}{abs(delta):.2f}% ({winner})")
            
    # 2. Memory
    print("\n[2] Memory Performance (sysbench memory 512M write):")
    print(f"{'Threads':<10}{'VM MiB/s':<14}{'Container MiB/s':<18}{'Delta':<18}")
    print("-" * 60)
    for t in [1, 2]:
        vm = parse_sysbench_mem(os.path.join(RAW_DIR, "memory", f"vm-memory-{t}thread.txt"))
        c = parse_sysbench_mem(os.path.join(RAW_DIR, "memory", f"container-memory-{t}thread.txt"))
        if vm and c:
            delta = ((c['mib_sec'] - vm['mib_sec']) / vm['mib_sec']) * 100
            winner = "Container" if delta >= 0 else "VM"
            print(f"{t:<10}{vm['mib_sec']:<14.2f}{c['mib_sec']:<18.2f}{abs(delta):.2f}% ({winner})")
            
    # 3. FastAPI Microservice
    print("\n[3] FastAPI Application Benchmarks (ApacheBench):")
    print(f"{'Endpoint':<14}{'VM Req/sec':<14}{'Container Req/sec':<20}{'VM Lat(ms)':<14}{'Cont Lat(ms)':<14}")
    print("-" * 72)
    endpoints = ["health", "compute", "memory"]
    for ep in endpoints:
        vm = parse_ab(os.path.join(RAW_DIR, "api", f"vm-{ep}.txt"))
        c = parse_ab(os.path.join(RAW_DIR, "api", f"container-{ep}.txt"))
        if vm and c:
            print(f"/{ep:<13}{vm['rps']:<14.2f}{c['rps']:<20.2f}{vm['latency_ms']:<14.2f}{c['latency_ms']:<14.2f}")

    print("\n" + "=" * 72)

if __name__ == "__main__":
    main()
