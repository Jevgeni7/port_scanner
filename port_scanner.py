import argparse
import socket
import threading
import time

# Create argument parser
parser = argparse.ArgumentParser(description='Scan for open ports on a target machine. Port scanning can be an invasive activity and might be unlawful or unethical without the owner\'s consent. Always seek proper authorization before performing any type of network testing or port scanning.')

# Add arguments
parser.add_argument('host', help='Target IP address or hostname')
parser.add_argument('-p', '--ports', type=str, default='1-1024', help='Range of ports to scan (default: 1-1024)')
parser.add_argument('-o', '--output', type=str, help='Output file')

# Parse arguments
args = parser.parse_args()

# Parse port range
start_port, end_port = map(int, args.ports.split('-'))

# Initialize list to store open ports
open_ports = []
progress = 0

# Define function to check if a single port is open
def check_port(port):
    global progress
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((args.host, port))
    if result == 0:
        open_ports.append(port)
    sock.close()
    progress += 1

# Define function to run port scan using multiple threads
def run_port_scan():
    max_threads = 64
    threads = []
    # Loop over ports and start a new thread to check each port
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=check_port, args=(port,))
        threads.append(t)
        t.start()
        # If the maximum number of threads is reached, wait for them to complete before starting new ones
        if len(threads) == max_threads:
            for t in threads:
                t.join()
                print_progress(progress, end_port - start_port + 1)
            threads = []
    # Wait for any remaining threads to complete
    for t in threads:
        t.join()
        print_progress(progress, end_port - start_port + 1)

# Define function to print progress bar
def print_progress(count, total):
    bar_len = 100
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)
    print(f'[{bar}] {percents}%\r', end='', flush=True)

# Run port scan and time it
start_time = time.time()
run_port_scan()
end_time = time.time()

# Output results to console or file
if open_ports:
    output_str = "\nOpen ports:\n" + '\n'.join(map(str, open_ports))
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_str)
        print(f"\nResults written to {args.output}")
    else:
        print(output_str)
else:
    if args.output:
        with open(args.output, 'w') as f:
            f.write("No open ports found")
        print(f"\nNo open ports found. Results written to {args.output}")
    else:
        print("\nNo open ports found")

# Output execution time
print(f"Execution time: {end_time - start_time:.2f} seconds")
