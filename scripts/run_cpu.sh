#!/usr/bin/env bash
# run_cpu.sh: Automated CPU benchmark execution using sysbench
set -e

OUT_DIR=${1:-"results/raw/cpu"}
mkdir -p "$OUT_DIR"

THREADS=(1 2 4 8)
TEST_TIME=30
PRIME_LIMIT=20000

echo "=== Starting CPU Benchmark (Threads: ${THREADS[*]}, Time: ${TEST_TIME}s, Prime: ${PRIME_LIMIT}) ==="

for t in "${THREADS[@]}"; do
    echo "Running sysbench CPU with $t thread(s)..."
    sysbench cpu \
        --threads="$t" \
        --cpu-max-prime="$PRIME_LIMIT" \
        --time="$TEST_TIME" \
        run > "$OUT_DIR/cpu-${t}thread.txt"
    echo "Saved to $OUT_DIR/cpu-${t}thread.txt"
done

echo "=== CPU Benchmark Complete ==="
