import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

labels = []
values = []

for log_path in sys.argv[1:]:
    scheme = os.path.basename(log_path).split('_')[0].capitalize()
    folder = os.path.basename(os.path.dirname(log_path))

    if folder.startswith("1mbps"):
        scheme = "1Mbps " + scheme
    elif folder.startswith("50mbps"):
        scheme = "50Mbps " + scheme

    total = 0
    dropped = 0

    with open(log_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            try:
                is_dropped = int(parts[3])
                total += 1
                if is_dropped == 1:
                    dropped += 1
            except:
                continue

    loss_rate = (100.0 * dropped / total) if total > 0 else 0
    labels.append(scheme)
    values.append(loss_rate)

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='salmon')
plt.ylabel('Packet Loss Rate (%)')
plt.title('Loss Rate per Scheme')
plt.xticks(rotation=0)
plt.ylim(0, max(values) * 1.2 if values else 1)
plt.tight_layout()
plt.savefig('loss_rate.png')
print("Saved: loss_rate.png")
