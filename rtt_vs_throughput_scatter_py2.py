import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

def extract_avg_rtt(log_path):
    rtts = []
    with open(log_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) == 4:
                rtts.append(float(parts[0]) / 1000.0)  
    return sum(rtts) / len(rtts) if rtts else 0

def extract_avg_throughput(log_path):
    bytes_total = 0
    start = None
    end = None
    with open(log_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) == 4:
                t = float(parts[0]) / 1000.0  
                size = int(parts[2])
                if start is None:
                    start = t
                end = t
                bytes_total += size
    if start is None or end is None or end == start:
        return 0
    duration = end - start
    return (bytes_total * 8) / duration / 1e6  

rtts = []
tputs = []
labels = []

for i in range(0, len(sys.argv[1:]), 2):
    uplink = sys.argv[1 + i]
    downlink = sys.argv[1 + i + 1]

    scheme = os.path.basename(uplink).split('_')[0].capitalize()
    folder = os.path.basename(os.path.dirname(uplink))
    label = ("1Mbps " if folder.startswith("1mbps") else "50Mbps ") + scheme
    labels.append(label)

    rtt = extract_avg_rtt(uplink)
    tput = extract_avg_throughput(downlink)
    rtts.append(rtt)
    tputs.append(tput)

plt.figure(figsize=(8, 6))
plt.scatter(rtts, tputs, s=100, c='purple')

for i, label in enumerate(labels):
    plt.text(rtts[i], tputs[i] + 0.2, label, ha='center', fontsize=8)

plt.xlabel("Average RTT (sec)")
plt.ylabel("Average Throughput (Mbps)")
plt.title("RTT vs Throughput Comparison")
plt.grid(True)
plt.tight_layout()
plt.savefig("rtt_vs_throughput.png")
print("Saved: rtt_vs_throughput.png")
