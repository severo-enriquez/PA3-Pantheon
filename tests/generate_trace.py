import sys

bandwidth_mbps = float(sys.argv[1])     
duration_secs = int(sys.argv[2])        
outfile = sys.argv[3]                 

bits_per_ms = (bandwidth_mbps * 1000000.0) / 1000.0
bytes_per_ms = bits_per_ms / 8.0
packet_size = 1500.0   
accumulator = 0.0
trace = []

for ms in range(duration_secs * 1000):
    accumulator += bytes_per_ms
    while accumulator >= packet_size:
        trace.append(ms)
        accumulator -= packet_size

with open(outfile, 'w') as f:
    for t in trace:
        f.write("%d\n" % t)
