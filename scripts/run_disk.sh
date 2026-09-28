#!/usr/bin/env bash
# run_disk.sh: Automated Disk I/O benchmarking using fio
set -e

OUT_DIR=${1:-"results/raw/disk"}
mkdir -p "$OUT_DIR"

SIZE="512M"
RUNTIME=30

echo "=== Starting Disk I/O Benchmark (Size: $SIZE, Runtime: ${RUNTIME}s) ==="

echo "1. Running Sequential Read..."
fio --name=seqread --ioengine=posixaio --rw=read --bs=1M --size="$SIZE" \
    --numjobs=1 --runtime="$RUNTIME" --time_based --direct=1 > "$OUT_DIR/seq-read.txt"
rm -f seqread.*

echo "2. Running Sequential Write..."
fio --name=seqwrite --ioengine=posixaio --rw=write --bs=1M --size="$SIZE" \
    --numjobs=1 --runtime="$RUNTIME" --time_based --direct=1 > "$OUT_DIR/seq-write.txt"
rm -f seqwrite.*

echo "3. Running Random Read (4K)..."
fio --name=randread --ioengine=posixaio --rw=randread --bs=4k --size="$SIZE" \
    --numjobs=1 --iodepth=4 --runtime="$RUNTIME" --time_based --direct=1 > "$OUT_DIR/rand-read.txt"
rm -f randread.*

echo "4. Running Random Write (4K)..."
fio --name=randwrite --ioengine=posixaio --rw=randwrite --bs=4k --size="$SIZE" \
    --numjobs=1 --iodepth=4 --runtime="$RUNTIME" --time_based --direct=1 > "$OUT_DIR/rand-write.txt"
rm -f randwrite.*

echo "=== Disk Benchmark Complete ==="
