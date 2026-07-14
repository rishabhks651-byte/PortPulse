import time
from tqdm import tqdm # Suggestion: Use tqdm or similar library for progress bars

class UIManager:
    """Manages user feedback, ensuring the UI is clean and non-minimalist."""

    def __init__(self):
        self.last_update_time = 0
        print("--- UX Initialized ---")

    def start_scan_display(self, target, scan_params):
        """Initial welcome display before scanning starts."""
        print("\n=============================================")
        print("| PORTPULSE SCANNING INITIATED             |")
        print("=============================================")

        # Display active flags in a visually appealing way
        display = f"Target: {target}\n"
        if scan_params['ping']: display += "-> Ping Scan Active\n"
        if scan_params['version_check']: display += "-> Service Versioning Enabled\n"
        if scan_params.get('os_detect'): display += "-> OS Detection Active\n"
        print(display)
        print("---------------------------------------------\n")


    def update_progress(self, current_host, total_hosts):
        """Updates progress visually (replaces simple print statements)."""
        # Use tqdm or a custom text-based bar for better UX
        print(f"\r[Progress] Scanning {current_host}/{total_hosts}...", end="", flush=True)

    def display_status(self, status_msg):
        """Logs important events (warnings/successes)."""
        timestamp = time.strftime("[%H:%M:%S]")
        print(f"\n{timestamp} [STATUS] {status_msg}")

# If using tqdm, the entire loop in portpulse_main.py would wrap the scanner call:
# with tqdm(total=len(targets), desc="Scanning Targets") as tbar:
#     for target in targets:
#         result = self.scanner.scan_single(target, scan_params)
#         tbar.update(1)
