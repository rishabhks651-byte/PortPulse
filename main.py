#!/usr/bin/env python3
import argparse
import sys
from target_resolver import TargetResolver
from scanner_engine import ScannerEngine
from reporting import Reporter
from ui_manager import UIManager
# from config import DEFAULT_PORTS # Assuming config is set up

class PortPulse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="PortPulse: Advanced Network Surveyor.",
            formatter_class=argparse.RawTextHelpFormatter
        )
        self._setup_arguments()
        self.resolver = TargetResolver()
        self.scanner = ScannerEngine()
        self.reporter = Reporter()
        self.ui = UIManager()

    def _setup_arguments(self):
        # --- TARGET SPECIFICATION ---
        group_target = self.parser.add_argument_group('Target Specification')
        group_target.add_argument('targets', nargs='*', default=[], 
                                    help="Hostnames, IP addresses, or ranges (e.g., scanme.nmap.org, 192.168.0.1).")

        # Optional Flags for Targets
        group_target.add_argument('-iL', '--input-file', help="Input list of hosts/networks from file.")
        group_target.add_argument('-iR', '--random-range', help="Select random targets within a range (e.g., 192.168.0.0/24).")
        group_target.add_argument('--exclude', help="Exclude specific hosts/networks list.")
        group_target.add_argument('--exclude-file', help="Exclude list from file.")

        # --- HOST DISCOVERY ---
        group_host = self.parser.add_argument_group('Host Discovery & Reachability')
        group_host.add_argument('-sL', '--list-scan', action='store_true', help="List only targets (no port scan).")
        group_host.add_argument('-sn', '--ping-scan', action='store_true', help="Ping Scan: Disable actual port scanning.")
        group_host.add_argument('-Pn', '--treat-online', action='store_true', help="Treat all hosts as online (skip host discovery).")
        # Add PS/PA/PU/PY for discovery probes here, mapping to custom logic
        group_host.add_argument('--disco-probe', choices=['PS', 'PA', 'PU'], 
                                 help="Specific discovery probes (SYN/ACK, UDP, SCTP).")

        # --- SCAN TECHNIQUES ---
        group_scan = self.parser.add_argument_group('Scan Techniques')
        group_scan.add_argument('-sS', '--syn-scan', action='store_true', help="TCP SYN Scan.")
        group_scan.add_argument('-sT', '--connect-scan', action='store_true', help="TCP Connect() Scan.")
        # ... add other -sX, -sU, etc., mappings here ...

        # --- PORT SPECIFICATION & ORDER ---
        group_port = self.parser.add_argument_group('Port Specification')
        group_port.add_argument('-p', '--ports', help="Specify ports (e.g., 22;1-100,8080).")
        group_port.add_argument('--exclude-ports', help="Ports to exclude from scanning.")
        group_port.add_argument('-F', '--fast-mode', action='store_true', help="Fast mode: Scan fewer ports than default.")
        group_port.add_argument('-r', '--sequential', action='store_true', help="Scan ports sequentially (non-random).")

        # --- SERVICE/VERSION DETECTION ---
        group_service = self.parser.add_argument_group('Service Detection')
        group_service.add_argument('-sV', '--version', action='store_true', help="Probe open ports to determine service/version info.")
        group_service.add_argument('--version-intensity', type=int, default=3, 
                                    help="Version scan intensity (0=light to 9=all).")

        # --- SCRIPT SCAN ---
        group_script = self.parser.add_argument_group('Script Scanning')
        group_script.add_argument('-sC', '--default-scripts', action='store_true', help="Run default NSE scripts.")
        group_script.add_argument('--custom-scripts', help="Specify custom Lua/script files or categories.")

        # --- OS DETECTION & MISC ---
        group_misc = self.parser.add_argument_group('OS Detection & Misc')
        group_misc.add_argument('-O', '--os-detection', action='store_true', help="Enable OS detection.");
        group_misc.add_argument('-A', '--all-scan', action='store_true', help="All-in-one scan (OS, Version, Scripts, Trace).");
        group_misc.add_argument('--traceroute', action='store_true', help="Trace hop path to each host.");

        # --- OUTPUT & TIMING ---
        group_output = self.parser.add_argument_group('Output & Verbosity')
        group_output.add_argument('-oN', '--output-normal', help="Output scan results in normal format.")
        group_output.add_argument('-oL', '--output-list', help="Output scan results in key/value list format.")
        group_output.add_argument('-v', '--verbose', action='store_true', help="Increase verbosity level.");
        group_output.add_argument('--resume', help="Resume an aborted scan from file.");

        self.args = self.parser.parse_args()

    def run(self):
        """Main execution flow."""
        print("--- PortPulse Initializing ---")

        # 1. Resolve Targets
        targets = list(self.resolver.resolve(self.args.targets, self.args.input_file))
        if not targets:
            print("[ERROR] No valid targets specified or resolved.")
            return

        print(f"[*] Resolved {len(targets)} unique targets to scan.")

        # 2. Prepare Scan Parameters
        scan_params = {
            'ports': self._parse_ports(self.args),
            'techniques': ['SYN'], # Default mechanism based on flags
            'version_check': self.args.version,
            'os_detect': self.args.os_detection,
            # ... other params mapped from args ...
        }

        # 3. Execute Scanning Loop
        all_results = []
        for target in targets:
            print(f"\n[+] Scanning Target: {target}")

            # High verbosity update on the UI manager while scanning
            self.ui.start_scan_display(target, scan_params) 

            result = self.scanner.scan_single(target, scan_params)
            all_results.append({'host': target, 'data': result})

        # 4. Reporting
        self.reporter.generate_report(all_results, self.args)


    def _parse_ports(self, args):
        """Helper to consolidate port flags."""
        if args.ports:
            return {'primary': args.ports}
        # Add logic for -F, --top-ports etc. here
        return {}

if __name__ == "__main__":
    portpulse = PortPulse()
    try:
        portpulse.run()
    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {e}", file=sys.stderr)
