# Port Scanner

A simple Python script that scans for open ports on a target machine.

## Usage

To use the port scanner, open your command line interface (CLI) in the directory containing the `port_scanner.py` file and run the following command:

python port_scanner.py &lt;host&gt;

Replace `<host>` with the IP address or hostname of the target machine you want to scan.

You can also specify a range of ports to scan using the `-p` or `--ports` option. The default range is 1-1024. For example:

python port_scanner.py &lt;host&gt; -p 1-65535

To save the results to a file, use the `-o` or `--output` option followed by the filename. For example:

python port_scanner.py &lt;host&gt; -o results.txt

### Example

To scan for open ports on your local machine, run the following command:

python port_scanner.py 127.0.0.1

## Disclaimer

Port scanning can be an invasive activity and might be unlawful or unethical without the owner's consent. Always seek proper authorization before performing any type of network testing or port scanning.
