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
        avg_rtt = 0.2  
    elif folder.startswith("50mbps"):
        scheme = "50Mbps " + scheme
        avg_rtt = 0.01  
    else:
        avg_rtt = 0

    labels.append(scheme)
    values.append(avg_rtt)

plt.figure(figsize=(8, 4))
plt.bar(labels, values, color='skyblue')
plt.ylabel('Average RTT (seconds)')
plt.title('Average RTT per Scheme')
plt.xticks(rotation=0)
plt.ylim(0, 0.25)
plt.tight_layout()
plt.savefig('avg_rtt_configured.png')
print("Saved: avg_rtt_configured.png")
