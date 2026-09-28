#!/usr/bin/env bash
# run_network.sh: Automated Network throughput benchmarking using iperf3
set -e

MODE=${1:-"client"}
TARGET_IP=${2:-"127.0.0.1"}
OUT_FILE=${3:-"network_benchmark.txt"}
DURATION=30

if [ "$MODE" = "server" ]; then
    echo "Starting iperf3 server on port 5201..."
    iperf3 -s
elif [ "$MODE" = "client" ]; then
    echo "Running iperf3 client connecting to $TARGET_IP for ${DURATION}s..."
    iperf3 -c "$TARGET_IP" -t "$DURATION" | tee "$OUT_FILE"
    echo "Benchmark output saved to $OUT_FILE"
else
    echo "Usage: $0 [server|client] [target_ip] [output_file]"
    exit 1
fi
