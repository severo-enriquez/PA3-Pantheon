import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

log_file = 'experiment_logs/50mbps_vegas/vegas_uplink.log'
scheme = 'vegas'

times = []
sizes = []

with open(log_file) as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        t = float(parts[0])
        size = int(parts[2])
        times.append(t)
        sizes.append(size)

bins = {}
for t, size in zip(times, sizes):
    sec = int(t)
    bins[sec] = bins.get(sec, 0) + size

throughput_times = sorted(bins.keys())
throughput_mbps = [bins[t] * 8.0 / 1e6 for t in throughput_times]

plt.figure(figsize=(10, 5))
plt.plot(throughput_times, throughput_mbps, marker='o')
plt.title('%s Throughput Over Time' % scheme.capitalize())
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbps)')
plt.grid(True)
plt.tight_layout()
plt.savefig('%s_throughput.png' % scheme)
print("Saved: %s_throughput.png" % scheme)
