FROM ubuntu:22.04

# Avoid interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# Install core benchmarking tools, system profilers, and runtimes
RUN apt-get update && apt-get install -y \
    sysbench \
    fio \
    iperf3 \
    curl \
    python3 \
    python3-pip \
    htop \
    procps \
    iproute2 \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /benchmarks

CMD ["/bin/bash"]
