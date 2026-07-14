# ⚡ PortPulse

PortPulse is a high-performance, multi-threaded network diagnostics tool designed to map open ports and identify active services with precision. Built with a modern, feature-rich dashboard UI, it bridges the gap between raw command-line power and beautiful data visualization.

## Features
- **High-Speed Multi-Threading:** Scan hundreds of ports concurrently.
- **Service Detection:** Automatically resolves common port numbers to their standard services.
- **Rich Dashboard UI:** Features real-time progress bars, live status logs, and a structured data table.
- **Smart Validation:** Built-in safeguards for IP addresses and port ranges.

## Installation & Usage

1. Install the required dependencies:
   ```bash
   pip install customtkinter
   pip install tqdm
   
## 📚 Core Command Examples

    Basic Full Scan:

    python portpulse_main.py -sS -sV scanme.nmap.org

    Scan a Range with Specific Ports and Versioning:

    python portpulse_main.py 192.168.0.0/24 -p 80,443 --version-intensity 5 -oN results.txt

    Perform Ping Sweep only:

    python portpulse_main.py scanme.nmap.org -sn

