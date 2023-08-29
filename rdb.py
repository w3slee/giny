import psutil
from prettytable import PrettyTable
from termcolor import colored
import time
import platform

def get_open_ports():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("0.0.0.0", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port
    except Exception:
        return None

def get_wifi_status():
    if platform.system() == "Darwin":  # macOS specific
        try:
            from pywifi import PyWiFi

            wifi = PyWiFi()
            iface = wifi.interfaces()[0]
            if iface.status() == 4:  # 4 means connected
                ssid = iface.scan_results()[0].ssid
                return f"Connected to {ssid}"
            else:
                return "Disconnected"
        except Exception:
            return "Disconnected"
    else:
        return "Unknown"

def get_ethernet_status():
    try:
        import psutil
        stats = psutil.net_if_stats()
        if "en0" in stats:  # "en0" is the default Ethernet interface on macOS
            return "Available"
        else:
            return "Not Available"
    except Exception:
        return "Not Available"

def get_ram_usage():
    ram = psutil.virtual_memory()
    return f"{ram.available / (1024 ** 3):.2f} GB available, {ram.used / (1024 ** 3):.2f} GB used"

def get_top_processes(num_processes=3):
    processes = []
    for process in sorted(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)[:num_processes]:
        processes.append([process.info['pid'], process.info['name'], f"{process.info['cpu_percent']}%"])
    return processes

def display_dashboard():
    while True:
        open_ports = get_open_ports()
        wifi_status = get_wifi_status()
        ethernet_status = get_ethernet_status()
        ram_usage = get_ram_usage()
        top_processes = get_top_processes()

        table = PrettyTable()
        table.field_names = ["Category", "Status"]
        table.add_row(["Open Ports", str(open_ports)])
        table.add_row(["Wi-Fi Status", wifi_status])
        table.add_row(["Ethernet Status", ethernet_status])
        table.add_row(["RAM Usage", ram_usage])

        print(colored("System Information", "blue"))
        print(table)

        if top_processes:
            process_table = PrettyTable()
            process_table.field_names = ["PID", "Process Name", "CPU %"]
            for process in top_processes:
                process_table.add_row(process)

            print(colored("\nTop Processes", "blue"))
            print(process_table)

        time.sleep(5)  # Refresh every 5 seconds

if __name__ == "__main__":
    try:
        print("Running ginyp.py")
        display_dashboard()
    except KeyboardInterrupt:
        print("\nExiting...")

