import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python2 plot_all_throughput_py2.py <uplink_log1> <uplink_log2> ...")
    sys.exit(1)

plt.figure(figsize=(10, 5))

for log_path in sys.argv[1:]:
    parts = log_path.split('/')
    if len(parts) < 2:
        print("Skipping bad path: %s" % log_path)
        continue

    folder = parts[-2]
    scheme = os.path.basename(log_path).split('_')[0].capitalize()
    label = scheme

    if '50mbps' in folder:
        label += ' (50 Mbps)'
    elif '1mbps' in folder:
        label += ' (1 Mbps)'

    times = []
    sizes = []

    with open(log_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            fields = line.strip().split()
            if len(fields) != 4:
                continue
            t = float(fields[0])
            size = int(fields[2])
            times.append(t)
            sizes.append(size)

    bins = {}
    for t, s in zip(times, sizes):
        sec = int(t / 1000.0)
        bins[sec] = bins.get(sec, 0) + s

    time_vals = sorted(bins.keys())
    throughput = [bins[t] * 8.0 / 1e6 for t in time_vals]

    plt.plot(time_vals, throughput, label=label)

plt.title('Throughput Comparison (1 Mbps vs 50 Mbps)')
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbps)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('combined_throughput_all.png')
print("Saved: combined_throughput_all.png")
