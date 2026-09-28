import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Base directories relative to script location or project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PROC_DIR = os.path.join(PROJECT_DIR, 'results', 'processed')
FIG_DIR = os.path.join(PROJECT_DIR, 'results', 'figures')

os.makedirs(PROC_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. CPU Data & CSV Export
# -------------------------------------------------------------
cpu_data = [
    {'threads': 1, 'vm_eps': 515.84, 'c_eps': 517.19, 'vm_lat_avg': 1.94, 'c_lat_avg': 1.93, 'vm_lat_p95': 2.71, 'c_lat_p95': 2.76, 'vm_events': 15479, 'c_events': 15519},
    {'threads': 2, 'vm_eps': 883.55, 'c_eps': 894.38, 'vm_lat_avg': 2.26, 'c_lat_avg': 2.23, 'vm_lat_p95': 3.82, 'c_lat_p95': 3.43, 'vm_events': 26511, 'c_events': 26835},
    {'threads': 4, 'vm_eps': 928.17, 'c_eps': 900.45, 'vm_lat_avg': 4.30, 'c_lat_avg': 4.43, 'vm_lat_p95': 7.43, 'c_lat_p95': 7.56, 'vm_events': 27850, 'c_events': 27018},
    {'threads': 8, 'vm_eps': 905.17, 'c_eps': 914.42, 'vm_lat_avg': 8.82, 'c_lat_avg': 8.73, 'vm_lat_p95': 15.55, 'c_lat_p95': 15.83, 'vm_events': 27159, 'c_events': 27438}
]
df_cpu = pd.DataFrame(cpu_data)
df_cpu.to_csv(os.path.join(PROC_DIR, 'cpu_results.csv'), index=False)

# -------------------------------------------------------------
# 2. Memory Data & CSV Export
# -------------------------------------------------------------
mem_data = [
    {'threads': 1, 'vm_mib_sec': 9541.97, 'c_mib_sec': 5152.43, 'vm_ops_sec': 9541.97, 'c_ops_sec': 5152.43, 'vm_lat_avg': 0.09, 'c_lat_avg': 0.12, 'vm_lat_p95': 0.25, 'c_lat_p95': 0.32},
    {'threads': 2, 'vm_mib_sec': 9880.38, 'c_mib_sec': 6970.16, 'vm_ops_sec': 9880.38, 'c_ops_sec': 6970.16, 'vm_lat_avg': 0.16, 'c_lat_avg': 0.22, 'vm_lat_p95': 0.38, 'c_lat_p95': 0.69}
]
df_mem = pd.DataFrame(mem_data)
df_mem.to_csv(os.path.join(PROC_DIR, 'memory_results.csv'), index=False)

# -------------------------------------------------------------
# 3. Disk Data & CSV Export
# -------------------------------------------------------------
disk_data = [
    {'workload': 'Seq Read (1M)', 'vm_bw_mibs': 461.0, 'c_bw_mibs': 500.0, 'vm_iops': 461, 'c_iops': 500, 'vm_lat_ms': 2.16, 'c_lat_ms': 1.99},
    {'workload': 'Seq Write (1M)', 'vm_bw_mibs': 358.0, 'c_bw_mibs': 291.0, 'vm_iops': 358, 'c_iops': 291, 'vm_lat_ms': 2.78, 'c_lat_ms': 3.42},
    {'workload': 'Rand Read (4K)', 'vm_bw_mibs': 5.13, 'c_bw_mibs': 6.91, 'vm_iops': 1313, 'c_iops': 1767, 'vm_lat_ms': 0.75, 'c_lat_ms': 0.56},
    {'workload': 'Rand Write (4K)', 'vm_bw_mibs': 5.20, 'c_bw_mibs': 5.26, 'vm_iops': 1331, 'c_iops': 1346, 'vm_lat_ms': 0.74, 'c_lat_ms': 0.73}
]
df_disk = pd.DataFrame(disk_data)
df_disk.to_csv(os.path.join(PROC_DIR, 'disk_results.csv'), index=False)

# -------------------------------------------------------------
# 4. Network Data & CSV Export
# -------------------------------------------------------------
net_data = [
    {'role': 'Sender (30s)', 'vm_gbps': 14.1, 'c_gbps': 13.7, 'vm_transferred_gb': 49.3, 'c_transferred_gb': 47.9, 'vm_retr': 3, 'c_retr': 13},
    {'role': 'Receiver', 'vm_gbps': 14.1, 'c_gbps': 10.3, 'vm_transferred_gb': 49.3, 'c_transferred_gb': 47.9, 'vm_retr': 0, 'c_retr': 0}
]
df_net = pd.DataFrame(net_data)
df_net.to_csv(os.path.join(PROC_DIR, 'network_results.csv'), index=False)

# -------------------------------------------------------------
# 5. FastAPI Microservice Data & CSV Export
# -------------------------------------------------------------
api_data = [
    {'endpoint': '/health', 'requests': 10000, 'concurrency': 100, 'vm_rps': 419.79, 'c_rps': 371.07, 'vm_lat_ms': 238.21, 'c_lat_ms': 269.49, 'vm_transfer_kb': 67.24, 'c_transfer_kb': 59.43},
    {'endpoint': '/compute', 'requests': 1000, 'concurrency': 10, 'vm_rps': 12.24, 'c_rps': 10.76, 'vm_lat_ms': 817.31, 'c_lat_ms': 929.47, 'vm_transfer_kb': 2.07, 'c_transfer_kb': 1.82},
    {'endpoint': '/memory', 'requests': 1000, 'concurrency': 10, 'vm_rps': 16.43, 'c_rps': 14.40, 'vm_lat_ms': 608.50, 'c_lat_ms': 694.62, 'vm_transfer_kb': 2.63, 'c_transfer_kb': 2.31}
]
df_api = pd.DataFrame(api_data)
df_api.to_csv(os.path.join(PROC_DIR, 'api_results.csv'), index=False)

# -------------------------------------------------------------
# 6. Combined Summary CSV Export
# -------------------------------------------------------------
summary_data = [
    {'Category': 'CPU (1-thread)', 'Metric': 'Events/sec', 'VM_Value': 515.84, 'Container_Value': 517.19, 'Relative_Difference': '+0.26% (Container faster)'},
    {'Category': 'CPU (2-thread)', 'Metric': 'Events/sec', 'VM_Value': 883.55, 'Container_Value': 894.38, 'Relative_Difference': '+1.23% (Container faster)'},
    {'Category': 'CPU (4-thread)', 'Metric': 'Events/sec', 'VM_Value': 928.17, 'Container_Value': 900.45, 'Relative_Difference': '+3.08% (VM faster)'},
    {'Category': 'CPU (8-thread)', 'Metric': 'Events/sec', 'VM_Value': 905.17, 'Container_Value': 914.42, 'Relative_Difference': '+1.02% (Container faster)'},
    {'Category': 'Memory (1-thread)', 'Metric': 'MiB/sec', 'VM_Value': 9541.97, 'Container_Value': 5152.43, 'Relative_Difference': '+85.19% (VM faster)'},
    {'Category': 'Memory (2-thread)', 'Metric': 'MiB/sec', 'VM_Value': 9880.38, 'Container_Value': 6970.16, 'Relative_Difference': '+41.75% (VM faster)'},
    {'Category': 'Storage Seq Read', 'Metric': 'MiB/s', 'VM_Value': 461.0, 'Container_Value': 500.0, 'Relative_Difference': '+8.46% (Container faster)'},
    {'Category': 'Storage Seq Write', 'Metric': 'MiB/s', 'VM_Value': 358.0, 'Container_Value': 291.0, 'Relative_Difference': '+23.02% (VM faster)'},
    {'Category': 'Storage Rand Read', 'Metric': 'IOPS', 'VM_Value': 1313.0, 'Container_Value': 1767.0, 'Relative_Difference': '+34.58% (Container faster)'},
    {'Category': 'Storage Rand Write', 'Metric': 'IOPS', 'VM_Value': 1331.0, 'Container_Value': 1346.0, 'Relative_Difference': '+1.13% (Container faster)'},
    {'Category': 'Network Throughput (Sender)', 'Metric': 'Gbits/sec', 'VM_Value': 14.1, 'Container_Value': 13.7, 'Relative_Difference': '+2.92% (VM faster)'},
    {'Category': 'Network Throughput (Receiver)', 'Metric': 'Gbits/sec', 'VM_Value': 14.1, 'Container_Value': 10.3, 'Relative_Difference': '+36.89% (VM faster)'},
    {'Category': 'Network Retransmissions', 'Metric': 'Packets', 'VM_Value': 3.0, 'Container_Value': 13.0, 'Relative_Difference': 'Container had 4.33x more retransmits'},
    {'Category': 'FastAPI /health', 'Metric': 'Req/sec', 'VM_Value': 419.79, 'Container_Value': 371.07, 'Relative_Difference': '+13.13% (VM faster)'},
    {'Category': 'FastAPI /compute', 'Metric': 'Req/sec', 'VM_Value': 12.24, 'Container_Value': 10.76, 'Relative_Difference': '+13.75% (VM faster)'},
    {'Category': 'FastAPI /memory', 'Metric': 'Req/sec', 'VM_Value': 16.43, 'Container_Value': 14.40, 'Relative_Difference': '+14.10% (VM faster)'}
]
df_summary = pd.DataFrame(summary_data)
df_summary.to_csv(os.path.join(PROC_DIR, 'summary_comparison.csv'), index=False)

# -------------------------------------------------------------
# PLOT 1: CPU Scalability
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
x = np.arange(len(df_cpu['threads']))
w = 0.35

ax1.bar(x - w/2, df_cpu['vm_eps'], w, label='Virtual Machine (Host)', color='#2563EB', alpha=0.9)
ax1.bar(x + w/2, df_cpu['c_eps'], w, label='Docker Container', color='#10B981', alpha=0.9)
ax1.set_xlabel('Worker Threads', fontweight='bold', fontsize=11)
ax1.set_ylabel('Throughput (Events/sec)', fontweight='bold', fontsize=11)
ax1.set_title('CPU Throughput vs Thread Count (sysbench)', fontweight='bold', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(['1 Thread', '2 Threads', '4 Threads', '8 Threads'])
ax1.legend(frameon=True)
for i in range(len(x)):
    ax1.text(x[i] - w/2, df_cpu['vm_eps'][i] + 15, f"{df_cpu['vm_eps'][i]:.1f}", ha='center', fontsize=9)
    ax1.text(x[i] + w/2, df_cpu['c_eps'][i] + 15, f"{df_cpu['c_eps'][i]:.1f}", ha='center', fontsize=9)

ax2.plot(df_cpu['threads'], df_cpu['vm_lat_avg'], marker='o', linewidth=2.5, markersize=8, label='VM Avg Latency', color='#2563EB')
ax2.plot(df_cpu['threads'], df_cpu['c_lat_avg'], marker='s', linewidth=2.5, markersize=8, label='Container Avg Latency', color='#10B981')
ax2.plot(df_cpu['threads'], df_cpu['vm_lat_p95'], marker='^', linestyle='--', linewidth=1.5, label='VM 95th Percentile', color='#1D4ED8')
ax2.plot(df_cpu['threads'], df_cpu['c_lat_p95'], marker='v', linestyle='--', linewidth=1.5, label='Container 95th Percentile', color='#047857')
ax2.set_xlabel('Worker Threads', fontweight='bold', fontsize=11)
ax2.set_ylabel('Execution Latency (ms)', fontweight='bold', fontsize=11)
ax2.set_title('CPU Latency vs Thread Contention', fontweight='bold', fontsize=12)
ax2.set_xticks(df_cpu['threads'])
ax2.legend(frameon=True)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'cpu_scalability.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# PLOT 2: Memory Performance
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
x = np.arange(len(df_mem['threads']))
w = 0.35

ax1.bar(x - w/2, df_mem['vm_mib_sec'], w, label='Virtual Machine', color='#2563EB', alpha=0.9)
ax1.bar(x + w/2, df_mem['c_mib_sec'], w, label='Docker Container', color='#10B981', alpha=0.9)
ax1.set_xlabel('Memory Benchmark Threads', fontweight='bold', fontsize=11)
ax1.set_ylabel('Bandwidth (MiB/sec)', fontweight='bold', fontsize=11)
ax1.set_title('Memory Sequential Write Bandwidth (512MB Block=1M)', fontweight='bold', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(['1 Thread', '2 Threads'])
ax1.legend(frameon=True)
for i in range(len(x)):
    ax1.text(x[i] - w/2, df_mem['vm_mib_sec'][i] + 150, f"{df_mem['vm_mib_sec'][i]:.1f}", ha='center', fontsize=9)
    ax1.text(x[i] + w/2, df_mem['c_mib_sec'][i] + 150, f"{df_mem['c_mib_sec'][i]:.1f}", ha='center', fontsize=9)

ax2.bar(x - w/2, df_mem['vm_lat_avg'], w, label='VM Avg Latency', color='#3B82F6', alpha=0.9)
ax2.bar(x + w/2, df_mem['c_lat_avg'], w, label='Container Avg Latency', color='#34D399', alpha=0.9)
ax2.set_xlabel('Memory Benchmark Threads', fontweight='bold', fontsize=11)
ax2.set_ylabel('Average Latency (ms)', fontweight='bold', fontsize=11)
ax2.set_title('Memory Access Latency Comparison', fontweight='bold', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(['1 Thread', '2 Threads'])
ax2.legend(frameon=True)
for i in range(len(x)):
    ax2.text(x[i] - w/2, df_mem['vm_lat_avg'][i] + 0.005, f"{df_mem['vm_lat_avg'][i]:.2f} ms", ha='center', fontsize=9)
    ax2.text(x[i] + w/2, df_mem['c_lat_avg'][i] + 0.005, f"{df_mem['c_lat_avg'][i]:.2f} ms", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'memory_performance.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# PLOT 3: Disk I/O Performance
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
seq_labels = ['Seq Read (1M)', 'Seq Write (1M)']
vm_seq_bw = [461.0, 358.0]
c_seq_bw = [500.0, 291.0]
xs = np.arange(len(seq_labels))
ws = 0.35

ax1.bar(xs - ws/2, vm_seq_bw, ws, label='Virtual Machine', color='#2563EB', alpha=0.9)
ax1.bar(xs + ws/2, c_seq_bw, ws, label='Docker Container', color='#10B981', alpha=0.9)
ax1.set_ylabel('Sequential Bandwidth (MiB/s)', fontweight='bold', fontsize=11)
ax1.set_title('Storage Sequential I/O Bandwidth (fio)', fontweight='bold', fontsize=12)
ax1.set_xticks(xs)
ax1.set_xticklabels(seq_labels, fontweight='bold')
ax1.legend(frameon=True)
for i in range(len(xs)):
    ax1.text(xs[i] - ws/2, vm_seq_bw[i] + 10, f"{vm_seq_bw[i]:.0f} MiB/s", ha='center', fontsize=9)
    ax1.text(xs[i] + ws/2, c_seq_bw[i] + 10, f"{c_seq_bw[i]:.0f} MiB/s", ha='center', fontsize=9)

rand_labels = ['Rand Read (4K)', 'Rand Write (4K)']
vm_rand_iops = [1313, 1331]
c_rand_iops = [1767, 1346]
xr = np.arange(len(rand_labels))

ax2.bar(xr - ws/2, vm_rand_iops, ws, label='Virtual Machine', color='#2563EB', alpha=0.9)
ax2.bar(xr + ws/2, c_rand_iops, ws, label='Docker Container', color='#10B981', alpha=0.9)
ax2.set_ylabel('Random IOPS (Operations/sec)', fontweight='bold', fontsize=11)
ax2.set_title('Storage Random 4K IOPS (fio)', fontweight='bold', fontsize=12)
ax2.set_xticks(xr)
ax2.set_xticklabels(rand_labels, fontweight='bold')
ax2.legend(frameon=True)
for i in range(len(xr)):
    ax2.text(xr[i] - ws/2, vm_rand_iops[i] + 35, f"{vm_rand_iops[i]} IOPS", ha='center', fontsize=9)
    ax2.text(xr[i] + ws/2, c_rand_iops[i] + 35, f"{c_rand_iops[i]} IOPS", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'disk_io_performance.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# PLOT 4: Network Performance
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
net_labels = ['Sender Throughput', 'Receiver Throughput']
vm_net = [14.1, 14.1]
c_net = [13.7, 10.3]
xn = np.arange(len(net_labels))
wn = 0.35

ax1.bar(xn - wn/2, vm_net, wn, label='VM (Loopback 127.0.0.1)', color='#2563EB', alpha=0.9)
ax1.bar(xn + wn/2, c_net, wn, label='Container (Bridge 172.17.0.1)', color='#10B981', alpha=0.9)
ax1.set_ylabel('Bitrate (Gbits/sec)', fontweight='bold', fontsize=11)
ax1.set_title('Network Bitrate Comparison (iperf3 30s)', fontweight='bold', fontsize=12)
ax1.set_xticks(xn)
ax1.set_xticklabels(net_labels, fontweight='bold')
ax1.legend(frameon=True)
for i in range(len(xn)):
    ax1.text(xn[i] - wn/2, vm_net[i] + 0.3, f"{vm_net[i]:.1f} Gbps", ha='center', fontsize=9)
    ax1.text(xn[i] + wn/2, c_net[i] + 0.3, f"{c_net[i]:.1f} Gbps", ha='center', fontsize=9)

# Retransmissions
retr_labels = ['VM Loopback', 'Container Bridge']
retr_vals = [3, 13]
colors = ['#2563EB', '#F59E0B']
bars = ax2.bar(retr_labels, retr_vals, color=colors, width=0.45, alpha=0.9)
ax2.set_ylabel('TCP Retransmissions count', fontweight='bold', fontsize=11)
ax2.set_title('TCP Packet Retransmissions (Overhead / Loss)', fontweight='bold', fontsize=12)
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f'{int(yval)} pkts', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'network_performance.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# PLOT 5: FastAPI Microservice Performance
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.2))
endpoints = ['/health (c=100)', '/compute (c=10)', '/memory (c=10)']
vm_rps = [419.79, 12.24, 16.43]
c_rps = [371.07, 10.76, 14.40]
xa = np.arange(len(endpoints))
wa = 0.35

bars1 = ax1.bar(xa - wa/2, vm_rps, wa, label='Virtual Machine', color='#2563EB', alpha=0.9)
bars2 = ax1.bar(xa + wa/2, c_rps, wa, label='Docker Container', color='#10B981', alpha=0.9)
ax1.set_ylabel('Throughput (Requests / sec)', fontweight='bold', fontsize=11)
ax1.set_title('FastAPI Microservice Throughput (ab benchmark)', fontweight='bold', fontsize=12)
ax1.set_xticks(xa)
ax1.set_xticklabels(endpoints, fontweight='bold')
ax1.legend(frameon=True)
for i in range(len(xa)):
    ax1.text(xa[i] - wa/2, vm_rps[i] + (10 if i == 0 else 0.4), f"{vm_rps[i]:.1f}", ha='center', fontsize=9)
    ax1.text(xa[i] + wa/2, c_rps[i] + (10 if i == 0 else 0.4), f"{c_rps[i]:.1f}", ha='center', fontsize=9)

vm_lat = [238.21, 817.31, 608.50]
c_lat = [269.49, 929.47, 694.62]

ax2.bar(xa - wa/2, vm_lat, wa, label='VM Mean Latency', color='#3B82F6', alpha=0.9)
ax2.bar(xa + wa/2, c_lat, wa, label='Container Mean Latency', color='#34D399', alpha=0.9)
ax2.set_ylabel('Mean Latency (ms)', fontweight='bold', fontsize=11)
ax2.set_title('FastAPI Request Latency Comparison', fontweight='bold', fontsize=12)
ax2.set_xticks(xa)
ax2.set_xticklabels(endpoints, fontweight='bold')
ax2.legend(frameon=True)
for i in range(len(xa)):
    ax2.text(xa[i] - wa/2, vm_lat[i] + 15, f"{vm_lat[i]:.0f} ms", ha='center', fontsize=9)
    ax2.text(xa[i] + wa/2, c_lat[i] + 15, f"{c_lat[i]:.0f} ms", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fastapi_performance.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# PLOT 6: Comprehensive 6-Quadrant Dashboard
# -------------------------------------------------------------
fig, axs = plt.subplots(3, 2, figsize=(16, 15))
fig.suptitle('Complete Performance Evaluation: Virtual Machine vs Docker Container (Experiment 2)', fontsize=16, fontweight='bold', y=0.99)

# Panel 1: CPU Scalability
axs[0, 0].plot(df_cpu['threads'], df_cpu['vm_eps'], marker='o', linewidth=2.5, markersize=8, label='Virtual Machine', color='#2563EB')
axs[0, 0].plot(df_cpu['threads'], df_cpu['c_eps'], marker='s', linewidth=2.5, markersize=8, label='Docker Container', color='#10B981')
axs[0, 0].set_title('A: CPU Throughput Scalability (sysbench prime)', fontweight='bold')
axs[0, 0].set_xlabel('Threads')
axs[0, 0].set_ylabel('Events / Second')
axs[0, 0].set_xticks(df_cpu['threads'])
axs[0, 0].legend()

# Panel 2: Memory Bandwidth
xm = np.arange(len(df_mem['threads']))
axs[0, 1].bar(xm - 0.17, df_mem['vm_mib_sec'], 0.34, label='Virtual Machine', color='#2563EB')
axs[0, 1].bar(xm + 0.17, df_mem['c_mib_sec'], 0.34, label='Docker Container', color='#10B981')
axs[0, 1].set_title('B: Memory Write Bandwidth (MiB/s)', fontweight='bold')
axs[0, 1].set_xlabel('Threads')
axs[0, 1].set_ylabel('MiB / Second')
axs[0, 1].set_xticks(xm)
axs[0, 1].set_xticklabels(['1 Thread', '2 Threads'])
axs[0, 1].legend()

# Panel 3: Disk Throughput
all_disk_labels = ['Seq R', 'Seq W', 'Rand R', 'Rand W']
vm_disk_all = [461.0, 358.0, 5.13, 5.20]
c_disk_all = [500.0, 291.0, 6.91, 5.26]
xd = np.arange(len(all_disk_labels))
axs[1, 0].bar(xd - 0.17, vm_disk_all, 0.34, label='Virtual Machine', color='#2563EB')
axs[1, 0].bar(xd + 0.17, c_disk_all, 0.34, label='Docker Container', color='#10B981')
axs[1, 0].set_title('C: Storage Bandwidth (MiB/s) across I/O Profiles', fontweight='bold')
axs[1, 0].set_xlabel('I/O Pattern')
axs[1, 0].set_ylabel('Bandwidth (MiB/s)')
axs[1, 0].set_xticks(xd)
axs[1, 0].set_xticklabels(all_disk_labels)
axs[1, 0].legend()

# Panel 4: Network Bitrate & Retransmits
axs[1, 1].bar(xn - 0.17, vm_net, 0.34, label='VM Loopback', color='#2563EB')
axs[1, 1].bar(xn + 0.17, c_net, 0.34, label='Container Bridge', color='#10B981')
axs[1, 1].set_title('D: Network Bandwidth (iperf3 30s)', fontweight='bold')
axs[1, 1].set_xlabel('Measurement Endpoint')
axs[1, 1].set_ylabel('Bandwidth (Gbits/sec)')
axs[1, 1].set_xticks(xn)
axs[1, 1].set_xticklabels(['Sender', 'Receiver'])
axs[1, 1].legend()

# Panel 5: FastAPI Throughput
axs[2, 0].bar(xa - 0.17, vm_rps, 0.34, label='Virtual Machine', color='#2563EB')
axs[2, 0].bar(xa + 0.17, c_rps, 0.34, label='Docker Container', color='#10B981')
axs[2, 0].set_title('E: FastAPI Microservice Throughput (Req/sec)', fontweight='bold')
axs[2, 0].set_xlabel('Endpoint')
axs[2, 0].set_ylabel('Requests / Second')
axs[2, 0].set_xticks(xa)
axs[2, 0].set_xticklabels(['/health', '/compute', '/memory'])
axs[2, 0].legend()

# Panel 6: FastAPI Latency
axs[2, 1].bar(xa - 0.17, vm_lat, 0.34, label='VM Mean Latency', color='#3B82F6')
axs[2, 1].bar(xa + 0.17, c_lat, 0.34, label='Container Mean Latency', color='#34D399')
axs[2, 1].set_title('F: FastAPI Microservice Latency (ms)', fontweight='bold')
axs[2, 1].set_xlabel('Endpoint')
axs[2, 1].set_ylabel('Latency (ms)')
axs[2, 1].set_xticks(xa)
axs[2, 1].set_xticklabels(['/health', '/compute', '/memory'])
axs[2, 1].legend()

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(os.path.join(FIG_DIR, 'overall_performance_dashboard.png'), dpi=300)
plt.close()

print('All 6 CSVs and 6 publication-quality figures successfully created.')
