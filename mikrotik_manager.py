import tkinter as tk
from tkinter import scrolledtext, simpledialog
from netmiko import ConnectHandler
import time

class MikroTikManager:
    def __init__(self, root):
        self.root = root
        self.root.title("MikroTik RouterOS Manager")

        # Initialize net_connect attribute
        self.net_connect = None

        self.create_gui()

    def create_gui(self):
        # Entry for IP address
        self.ip_label = tk.Label(self.root, text="Router IP Address:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        # Entry for SSH Port
        self.port_label = tk.Label(self.root, text="SSH Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        # Button to connect
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_router)
        self.connect_button.pack()

        # Display output
        self.output_text = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.output_text.pack()

        # Additional buttons
        button_commands = [
            ("Change the IP address", self.change_ip),
            ("Configuration Backup", self.backup_configuration),
            ("IP Address Information", self.ip_address_info),
            ("Display Services and Ports", self.show_services_ports),
            ("Ping Test", self.ping_test),
            ("Toggle Safe Mode", self.toggle_safe_mode),
            ("Interface Status", self.interface_status),
            ("Reboot", self.reboot),
            ("Change Service Port", self.change_service_port),
        ]

        for text, command in button_commands:
            button = tk.Button(self.root, text=text, command=command)
            button.pack()

    def connect_to_router(self):
        router_ip = self.ip_entry.get()
        ssh_port = self.port_entry.get()

        # Prompt user for username and password
        username = simpledialog.askstring("Input", "Enter your MikroTik username:")
        password = simpledialog.askstring("Input", "Enter your MikroTik password:", show='*')

        device = {
            'device_type': 'mikrotik_routeros',
            'ip': router_ip,
            'port': ssh_port,
            'username': username,
            'password': password,
        }

        try:
            # Create SSH connection
            self.net_connect = ConnectHandler(**device)

            # Run a command (example: print system information)
            output = self.net_connect.send_command("/system resource print")
            self.output_text.insert(tk.END, output)

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")

    def change_ip(self):
        self.run_command("/interface ethernet set [find name=ether1] address=")

    def backup_configuration(self):
        self.run_command("/system backup save name=config_backup")

    def ip_address_info(self):
        self.run_command("/ip address print")

    def show_services_ports(self):
        self.run_command("/ip service print")

    def ping_test(self):
        host_to_ping = "127.0.0.1"  # Change to your desired host
        self.run_command(f"/ping {host_to_ping} count=4")

    def toggle_safe_mode(self):
        if self.net_connect is not None:
            try:     
                self.net_connect.write_channel('\x18')
                time.sleep(4)

                output = self.net_connect.read_channel()

                if "Safe Mode taken" in output:
                    self.output_text.insert(tk.END, "\nSafe mode is on.")
                else:
                    self.output_text.insert(tk.END, "\nSafe mode is deactivated.")

            except Exception as e:
                self.output_text.insert(tk.END, f"Error occurred whilst toggling the safe mode: {str(e)}")

        else:
            self.output_text.insert(tk.END, "Firstly, connect to the router!")

    def interface_status(self):
        self.run_command("/interface print detail")

    def reboot(self):
        self.run_command("/system reboot")

    def change_service_port(self):
        self.run_command("/ip service set telnet port=8888")

    def run_command(self, command):
        router_ip = self.ip_entry.get()
        ssh_port = self.port_entry.get()

        try:
            # Run the specified command
            output = self.net_connect.send_command(command)
            self.output_text.insert(tk.END, output)

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MikroTikManager(root)
    root.mainloop()
