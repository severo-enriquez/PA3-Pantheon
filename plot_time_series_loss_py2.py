import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

def compute_loss_over_time(log_path):
    loss_by_time = {}
    with open(log_path) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            try:
                timestamp = float(parts[0]) / 1000.0
                dropped = int(parts[3])
                sec = int(timestamp)
                if sec not in loss_by_time:
                    loss_by_time[sec] = {'sent': 0, 'dropped': 0}
                loss_by_time[sec]['sent'] += 1
                if dropped:
                    loss_by_time[sec]['dropped'] += 1
            except:
                continue
    x = sorted(loss_by_time.keys())
    y = [100.0 * loss_by_time[t]['dropped'] / loss_by_time[t]['sent']
         if loss_by_time[t]['sent'] > 0 else 0 for t in x]
    return x, y

plt.figure(figsize=(10, 5))

for log_path in sys.argv[1:]:
    scheme = os.path.basename(log_path).split('_')[0].capitalize()
    folder = os.path.basename(os.path.dirname(log_path))
    label = ("1Mbps " if folder.startswith("1mbps") else "50Mbps ") + scheme

    x, y = compute_loss_over_time(log_path)
    plt.plot(x, y, label=label)

plt.title('Loss Rate Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Loss Rate (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('loss_time_series.png')
print("Saved: loss_time_series.png")
