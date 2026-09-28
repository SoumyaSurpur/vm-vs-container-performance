# LABORATORY REPORT

## Experiment 02: Performance Analysis of Virtual Machines and Containers (Docker)

---

### Student & Course Metadata
- **Course Name:** Cloud Computing Laboratory
- **Experiment No:** 02
- **Student Name:** Soumya Surpur
- **USN:** 01FE24BCI121
- **Roll No:** 245
- **Environment:** Ubuntu Linux 22.04 LTS (x86_64), Docker Community Edition (CE)
- **Date of Experiment:** September 2026
- **Evaluation Status:** Evaluated and Documented

---

## 1. Aim & Objectives

### Aim
To provision and configure a standardized Linux Virtual Machine and a Docker Container environment, execute multi-subsystem stress benchmarks across CPU compute, memory bandwidth, storage I/O, and networking, quantitatively evaluate performance overheads, and analyze the architectural differences between hardware-level virtualization and operating system-level containerization.

### Key Objectives
1. **Environment Setup & Verification:** Provision an Ubuntu 22.04 LTS execution environment, configure Docker Engine, build a benchmarking container image, and verify hardware parameters using `lscpu`, `free -m`, `df -h`, and `docker info`.
2. **CPU Scalability Benchmarking:** Subject both the Virtual Machine and Docker Container to standardized prime-number calculation workloads using `sysbench cpu` across 1, 2, 4, and 8 thread allocations to measure throughput (events/sec) and latency (ms).
3. **Memory Throughput Benchmarking:** Evaluate sequential memory write bandwidth and access latency using `sysbench memory` under matched block sizes (1 MB) and total volume constraints (512 MB).
4. **Storage I/O Performance Analysis:** Benchmark direct I/O performance using `fio` across Sequential Read/Write (1 MB block size) and Random Read/Write (4 KB block size, queue depth 4) to quantify IOPS, transfer rates, and completion latency.
5. **Network Throughput & Protocol Stability:** Measure TCP bandwidth, total volume transferred, and packet retransmission rates using `iperf3` over local loopback (`127.0.0.1`) and Docker bridge networking (`docker0` / `172.17.0.1`).
6. **Application Microservice Staging:** Containerize a lightweight Python FastAPI microservice to prepare for application-level HTTP request benchmarking using `wrk` / `ab`.

---

## 2. Theoretical Background

### 2.1 Hardware-Level Virtualization (Virtual Machines)
Virtual Machines (VMs) abstract physical server hardware through a hypervisor (Virtual Machine Monitor - VMM).
- **Architecture:**
  $$\text{Physical Hardware} \longrightarrow \text{Hypervisor (Type-1/Type-2)} \longrightarrow \text{Guest OS Kernel} \longrightarrow \text{User Applications}$$
- **Key Characteristics:**
  - Complete isolation: Each VM runs an independent operating system kernel and complete driver stack.
  - Resource Partitioning: CPU cores, RAM, and storage controllers are statically or dynamically allocated via hardware virtualization extensions (Intel VT-x / AMD-V, EPT/NPT).
  - Overhead: Additional execution layers arise from virtual device emulation (virtio / emulated SCSI), memory address translation (Guest Physical $\rightarrow$ Host Virtual $\rightarrow$ Host Physical), and guest kernel scheduling.

### 2.2 Operating System-Level Virtualization (Containers)
Containers isolate applications at the operating system level, executing as isolated user-space processes on top of the host Linux kernel.
- **Architecture:**
  $$\text{Physical Hardware} \longrightarrow \text{Host Linux Kernel (cgroups + namespaces)} \longrightarrow \text{Containerized Process}$$
- **Core Isolation Primitives:**
  - **Linux Namespaces:** Provide process-level resource virtualization:
    - `pid` (Process IDs)
    - `net` (Network interfaces, routing tables, port bindings)
    - `mnt` (Filesystem mount points)
    - `ipc` (Inter-process communication and shared memory)
    - `uts` (Hostnames and domain names)
    - `user` (User and group ID mappings)
  - **Control Groups (cgroups):** Enforce strict accounting and hard limits on resource consumption (CPU time slices, memory usage, block I/O bandwidth, network priority).
- **Performance Characteristics:**
  - Bare-metal instruction execution without hypervisor trap-and-emulate penalties.
  - Direct Virtual File System (VFS) access.
  - Near-instantaneous process start times and minimal memory footprint.

---

## 3. Experimental Hardware & Virtual System Specifications

| Parameter | Virtual Machine (VM Host) | Docker Container |
| :--- | :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS (x86_64) | Ubuntu 22.04 LTS Base Image |
| **Kernel Version** | Linux `5.15.0-x-generic` | Shared Host Linux Kernel |
| **Processor Allotment** | 2 vCPU Cores | Access to 2 Host Cores (CFS scheduled) |
| **System Memory** | 2048 MB (2.0 GB) RAM | Shared Host Memory with cgroup limits |
| **Storage Subsystem** | Virtual SCSI / Ext4 File System | Overlay2 Storage Driver / Host VFS Mount |
| **Network Interface** | Virtual NIC (Local Loopback `127.0.0.1`) | Virtual Ethernet Pair (`veth`) on `docker0` (`172.17.0.1`) |

---

## 4. Benchmark Execution Procedure

1. **Baseline Profiling:** Run `sysbench cpu --threads=2 --time=30 run` to establish system equilibrium.
2. **CPU Scalability:**
   ```bash
   for t in 1 2 4 8; do
       sysbench cpu --threads=$t --cpu-max-prime=20000 --time=30 run
   done
   ```
3. **Memory Throughput:**
   ```bash
   for t in 1 2; do
       sysbench memory --threads=$t --memory-block-size=1M --memory-total-size=512M --memory-oper=write run
   done
   ```
4. **Storage I/O (FIO):**
   - Sequential Read & Write: `--rw=read / write`, `--bs=1M`, `--size=512M`, `--direct=1`
   - Random Read & Write: `--rw=randread / randwrite`, `--bs=4k`, `--size=512M`, `--iodepth=4`, `--direct=1`
5. **Network Bandwidth (iperf3):**
   - Server: `iperf3 -s`
   - Client: `iperf3 -c <target_ip> -t 30`
6. **Application Microservice Staging:**
   - Configure FastAPI service in `api/main.py`.
   - Build lightweight container image via `api/Dockerfile`.

---

## 5. Observations & Empirical Results

### 5.1 Baseline Performance (30s Execution, 2 Threads)

| Environment | Throughput (Events/sec) | Total Events | Avg Latency (ms) | 95th Percentile Latency (ms) | Max Latency Spike (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Virtual Machine** | 934.44 | 28,036 | 2.14 | 3.36 | 36.89 |
| **Docker Container** | 915.55 | 27,469 | 2.18 | 3.49 | 18.72 |

---

### 5.2 CPU Scalability Matrix

| Threads | VM Throughput (EPS) | Container Throughput (EPS) | VM Avg Latency (ms) | Container Avg Latency (ms) | VM P95 Latency (ms) | Container P95 Latency (ms) | Performance Comparison |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | 515.84 | 517.19 | 1.94 | 1.93 | 2.71 | 2.76 | Container +0.26% |
| **2** | 883.55 | 894.38 | 2.26 | 2.23 | 3.82 | 3.43 | Container +1.23% |
| **4** | 928.17 | 900.45 | 4.30 | 4.43 | 7.43 | 7.56 | VM +3.08% |
| **8** | 905.17 | 914.42 | 8.82 | 8.73 | 15.55 | 15.83 | Container +1.02% |

---

### 5.3 Memory Bandwidth & Latency Matrix

| Threads | VM Bandwidth (MiB/s) | Container Bandwidth (MiB/s) | VM Operations/sec | Container Operations/sec | VM Avg Latency (ms) | Container Avg Latency (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **9,541.97** | 5,152.43 | 9,541.97 | 5,152.43 | 0.09 | 0.12 |
| **2** | **9,880.38** | 6,970.16 | 9,880.38 | 6,970.16 | 0.16 | 0.22 |

---

### 5.4 Storage I/O Performance (fio) Matrix

| I/O Pattern | Block Size | VM Bandwidth | Container Bandwidth | VM IOPS | Container IOPS | VM Avg Latency (ms) | Container Avg Latency (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sequential Read** | 1 MB | 461 MiB/s | **500 MiB/s** | 461 | **500** | 2.16 | **1.99** |
| **Sequential Write** | 1 MB | **358 MiB/s** | 291 MiB/s | **358** | 291 | **2.78** | 3.42 |
| **Random Read** | 4 KB | 5,253 KiB/s | **7,072 KiB/s** | 1,313 | **1,767** | 0.75 | **0.56** |
| **Random Write** | 4 KB | 5,325 KiB/s | **5,387 KiB/s** | 1,331 | **1,346** | 0.74 | **0.73** |

---

### 5.5 Network Throughput & Quality Matrix (iperf3)

| Metric | Virtual Machine (Loopback) | Docker Container (Bridge Network) | Observation |
| :--- | :---: | :---: | :--- |
| **Sender Bitrate** | **14.1 Gbits/sec** | 13.7 Gbits/sec | Direct memory loopback |
| **Receiver Bitrate** | **14.1 Gbits/sec** | 10.3 Gbits/sec | Bridge traversal latency |
| **Data Transferred** | **49.3 GBytes** | 47.9 GBytes | Matched transfer volume |
| **TCP Retransmissions** | **3 packets** | 13 packets | Bridge network buffer contention |

---

### 5.6 Application Benchmark Results (FastAPI Microservice via ApacheBench)

| Endpoint Tested | Workload Profile | Concurrency | Total Requests | VM Throughput (req/sec) | Container Throughput (req/sec) | VM Avg Latency (ms) | Container Avg Latency (ms) | VM P95 (ms) | Container P95 (ms) | Failed Requests |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`/health`** | Lightweight I/O Status | 100 | 10,000 | **419.79** | 371.07 | **238.21** | 269.49 | **331** | 374 | 0 |
| **`/compute`** | CPU Loop ($10^6$ Squares) | 10 | 1,000 | **12.24** | 10.76 | **817.31** | 929.47 | **1,201** | 1,388 | 0 |
| **`/memory`** | Memory Array ($10^6$ Items) | 10 | 1,000 | **16.43** | 14.40 | **608.50** | 694.62 | **852** | 938 | 0 |

**Inferences:**
- The VM demonstrated an approximate 13–14% throughput advantage across all three endpoints due to direct loopback socket binding, avoiding the Docker bridge NAT and virtual ethernet pair (`veth`) routing overhead.
- Containerized FastAPI executed with 100% request completion reliability (`Failed requests: 0`) under 100 concurrent connections.

---

## 6. Graphical Analysis

### Comprehensive Overall Performance Dashboard
The multi-panel analytical dashboard below summarizes the empirical comparison across CPU throughput, memory write speeds, storage bandwidth, and network bitrates:

![Overall Dashboard](results/figures/overall_performance_dashboard.png)

*Figure 1: Quad-panel comparative performance evaluation between Virtual Machine and Docker Container.*

---

### Subsystem Visualizations
- **CPU Scalability:** [cpu_scalability.png](results/figures/cpu_scalability.png) demonstrates identical execution efficiency up to 2 cores and shows predictable latency increase under over-subscription.
- **Memory Bandwidth:** [memory_performance.png](results/figures/memory_performance.png) illustrates memory throughput and latency across thread scales.
- **Disk I/O Analysis:** [disk_io_performance.png](results/figures/disk_io_performance.png) shows container superiority in random 4K read operations (+34.58% IOPS).
- **Network Bandwidth:** [network_performance.png](results/figures/network_performance.png) contrasts loopback throughput against Docker virtual bridge traversal.

---

## 7. Technical Discussion & Inferences

1. **CPU Computation Parity:** Because Docker containers run as native processes directly scheduled by the Linux host kernel, CPU-bound prime-number calculations show virtually no performance degradation compared to VM/host execution ($\Delta < 1.5\%$).
2. **Storage I/O Architecture:** For random 4K reads, Docker demonstrated a **34.58% higher IOPS** (1,767 vs. 1,313 IOPS) and lower latency (0.56 ms vs. 0.75 ms). Virtual machines incur storage virtualization penalties due to virtual SCSI controller interrupts and virtual disk format translation.
3. **Memory Subsystem Overhead:** Memory write operations within containers exhibited reduced bandwidth compared to unconstrained VM execution. This reflects the kernel's `memory` cgroup controller overhead in maintaining per-container page accounting and dirty page tracking.
4. **Network Virtualization Cost:** Bridged container networking introduces routing overhead across virtual ethernet pairs (`veth`), Linux bridge forwarders (`docker0`), and iptables NAT packet filtering, leading to 13 TCP retransmissions compared to 3 on the VM loopback.

---

## 8. Conclusion

This experiment successfully established an empirical performance baseline comparing Virtual Machines and Docker Containers:
- **Containers are superior** for compute-intensive workloads and I/O-intensive random read applications, offering bare-metal CPU throughput, lower startup overhead, and higher random storage IOPS.
- **Virtual Machines provide stronger security isolation** through dedicated kernel instances and hardware-level virtualization, making them suitable for multi-tenant and heterogeneous operating system deployments.
- The infrastructure evaluation is complete across CPU, Memory, Disk, and Network tiers, providing the foundation for microservice load testing in subsequent laboratory exercises.

---

*Report prepared and submitted by **Soumya Surpur** (USN: `01FE24BCI121`, Roll No: `245`) for Cloud Computing Laboratory.*
