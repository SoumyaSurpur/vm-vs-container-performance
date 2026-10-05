import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CPU Scalability
# =========================

cpu = pd.read_csv("processed/cpu_scalability.csv")

plt.figure(figsize=(8, 5))

for environment in cpu["environment"].unique():
    data = cpu[cpu["environment"] == environment]
    plt.plot(
        data["threads"],
        data["events_per_second"],
        marker="o",
        linewidth=2,
        label=environment
    )

plt.xlabel("Number of Threads")
plt.ylabel("Events per Second")
plt.title("CPU Scalability: VM vs Docker")
plt.xticks([1, 2, 4, 8])
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/cpu_scalability.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# =========================
# API Scalability
# =========================

api = pd.read_csv("processed/api_scalability.csv")

plt.figure(figsize=(8, 5))

for environment in api["environment"].unique():
    data = api[api["environment"] == environment]
    plt.plot(
        data["connections"],
        data["requests_per_second"],
        marker="o",
        linewidth=2,
        label=environment
    )

plt.xlabel("Concurrent Connections")
plt.ylabel("Requests per Second")
plt.title("FastAPI Scalability: VM vs Docker")
plt.xticks([10, 50, 100, 200])
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/api_scalability.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Scalability graphs generated successfully.")
