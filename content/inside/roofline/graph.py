import matplotlib.pyplot as plt
import numpy as np
ai = np.logspace(-2, 2, 200)  # 0.01 to 100 ops/byte

bw_l1 = 4e9             # 4 GB/s
bw_dram = 1e9           # 1 GB/s
k_ops = 4 
k_bw = 8 
k_cycles = 7
perf_l1 = bw_l1 * ai
perf_dram = bw_dram * ai
peak_compute = 2e9      # 1 GOP/s
real_compute = (k_ops / k_cycles) * peak_compute      # 1 GOP/s

# Apply compute ceiling
perf_l1 = np.minimum(perf_l1, peak_compute)
perf_dram = np.minimum(perf_dram, peak_compute)

# -----------------------------
# Plot
# -----------------------------
plt.figure()

# Memory roofs
plt.loglog(ai, perf_l1, label="L1 Roof (4 GB/s)")
plt.loglog(ai, perf_dram, label="DRAM Roof (1 GB/s)")

# Compute roof
plt.axhline(peak_compute, linestyle='--', color="green" , label="Theoretical Compute Roof (1 GOP/s)")

plt.xlabel("Arithmetic Intensity (Ops/Byte)")
plt.ylabel("Performance (Ops/s)")

plt.legend()
plt.grid(True, which="both")

plt.savefig("roofline1.jpg", dpi=600)
# -----------------------------
# Example kernel: dot product
# -----------------------------
ai_dot = k_ops/k_bw
perf_dot = min(bw_l1 * ai_dot, peak_compute)

plt.scatter([ai_dot], [perf_dot],color="Red", edgecolors="black", linewidths=1)
plt.text(ai_dot, perf_dot, "Small N", fontsize=11, fontweight="bold")

perf_dot = min(bw_dram * ai_dot, peak_compute)
plt.scatter([ai_dot], [perf_dot], color="Red", edgecolors="black", linewidths=1) 
plt.text(ai_dot, perf_dot, "Large N", fontsize=11, fontweight="bold")

plt.savefig("roofline2.jpg", dpi=600)

plt.figure()

# Memory roofs
plt.loglog(ai, perf_l1, label="L1 Roof (4 GB/s)")
plt.loglog(ai, perf_dram, label="DRAM Roof (1 GB/s)")

# Compute roof
plt.axhline(peak_compute, linestyle='--', color="green" , label="Theoretical Compute Roof (2 GOP/s)")
plt.axhline(real_compute, linestyle='--', color="brown" , label="Kernel Compute Roof (1.14 GOP/s)")
plt.xlabel("Arithmetic Intensity (Ops/Byte)")
plt.ylabel("Performance (Ops/s)")

plt.legend()
plt.grid(True, which="both")

ai_dot = k_ops / k_bw
perf_dot = min(bw_l1 * ai_dot, real_compute)
plt.axvline(ai_dot, linestyle='--', color='black', label="Locality Wall (L1)")
plt.scatter([ai_dot], [perf_dot], color="magenta", edgecolors="black", linewidths=1, s=80)
plt.text(ai_dot, perf_dot, "A", fontsize=10, fontweight="bold")

ai_dot = k_ops / (k_bw * 4)
perf_dot = min(bw_dram * ai_dot, real_compute)
plt.axvline(ai_dot, linestyle='-.', color='black', label="Locality Wall (DRAM)")
plt.scatter([ai_dot], [perf_dot], color="magenta", edgecolors="black", linewidths=1, s=80)
plt.text(ai_dot, perf_dot, "B", fontsize=10, fontweight="bold")

ai_dot = k_ops / (k_bw * 2)
perf_dot = min(0.5*((bw_dram * ai_dot) + (bw_l1 * ai_dot)), real_compute)
plt.scatter([ai_dot], [perf_dot], color="magenta", edgecolors="black", linewidths=1, s=80)
plt.text(ai_dot, perf_dot, "C", fontsize=10, fontweight="bold")


k_ops_unrolled = 8 
k_cycles_unrolled = 10
k_bw_unrolled = 16
real_compute_unrolled = ( k_ops_unrolled / k_cycles_unrolled) * peak_compute
ai_dot = 10 / (k_bw_unrolled * 2)
perf_dot = min(0.5*((bw_dram * ai_dot) + (bw_l1 * ai_dot)), real_compute_unrolled)
plt.scatter([ai_dot], [perf_dot], color="magenta", edgecolors="black", linewidths=1, s=80)
plt.text(ai_dot, perf_dot, "D", fontsize=10, fontweight="bold")
plt.axhline(real_compute_unrolled, linestyle='--', color="Grey" , label="Kernel Compute Roof (Unrolling)")


plt.legend()
plt.savefig("roofline3.jpg", dpi=600)
