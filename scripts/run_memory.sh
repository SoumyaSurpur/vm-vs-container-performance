#!/usr/bin/env bash
# run_memory.sh: Automated Memory throughput benchmark using sysbench
set -e

OUT_DIR=${1:-"results/raw/memory"}
mkdir -p "$OUT_DIR"

THREADS=(1 2)
BLOCK_SIZE="1M"
TOTAL_SIZE="512M"
OPERATION="write"

echo "=== Starting Memory Benchmark (Threads: ${THREADS[*]}, Block: $BLOCK_SIZE, Total: $TOTAL_SIZE) ==="

for t in "${THREADS[@]}"; do
    echo "Running sysbench memory with $t thread(s)..."
    sysbench memory \
        --threads="$t" \
        --memory-block-size="$BLOCK_SIZE" \
        --memory-total-size="$TOTAL_SIZE" \
        --memory-oper="$OPERATION" \
        run > "$OUT_DIR/memory-${t}thread.txt"
    echo "Saved to $OUT_DIR/memory-${t}thread.txt"
done

echo "=== Memory Benchmark Complete ==="
