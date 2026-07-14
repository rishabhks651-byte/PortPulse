from datetime import datetime

class Reporter:
    """Handles all output formatting, managing CLI display vs. file persistence."""

    def __init__(self):
        self.report_data = []

    def generate_report(self, results, args):
        print("\n=======================================")
        print("         PORTPULSE SCAN REPORT")
        print("=======================================\n")

        # 1. CLI Display (Default Mode)
        if args.verbose:
            print("--- Verbose Summary ---")
            for res in results:
                print(f"Host: {res['host']} | Status: {self._summarize_host(res)}")

        # 2. File Outputs
        file_output = None
        if args.output_normal:
            file_output = "Normal Report Mode"
        elif args.output_list:
            file_output = "Key/Value List Mode"

        if file_output and file_output != "None":
            print(f"\n[FILE MODE] Preparing to write to Normal/List output...")
            # Logic to generate structured text for the specified format
            pass 

        if args.all_scan:
             print("\n--- All-In-One Comprehensive Report Generated ---")


    def _summarize_host(self, result):
        """Creates a readable string summarizing one host's state."""
        summary = f"Host {result['host']}: "

        # Check if any ports are open
        open_ports = [port for port, data in result.get('data', {}).items() 
                      if data.get('state') == 'Open']

        status = ", ".join(open_ports) if open_ports else "None Found"
        summary += f"Ports: {status}. Services: {result['services']}"
        return summary

    def output_to_file(self, filename):
        """Writes the aggregated report to disk based on format."""
        # Implementation using file writers for -oN, -oL, etc.
        pass
