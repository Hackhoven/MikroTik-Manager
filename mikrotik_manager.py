import tkinter as tk
from tkinter import scrolledtext, simpledialog
import paramiko

class MikroTikManager:
    def __init__(self, root):
        self.root = root
        self.root.title("MikroTik RouterOS Manager")

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
            ("Change IP", self.change_ip),
            ("Backup Configuration", self.backup_configuration),
            ("IP Address Info", self.ip_address_info),
            ("Show Services and Ports", self.show_services_ports),
            ("Ping Test", self.ping_test),
            ("Enable/Disable Safe Mode", self.toggle_safe_mode),
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

        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the MikroTik Router
            ssh.connect(router_ip, port=ssh_port, username=username, password=password)

            # Run a command (example: print system information)
            stdin, stdout, stderr = ssh.exec_command("/system resource print")

            # Display the output
            output = stdout.read().decode("utf-8")
            self.output_text.insert(tk.END, output)

            # Close the SSH connection
            ssh.close()

        except paramiko.AuthenticationException:
            self.output_text.insert(tk.END, "Authentication failed. Please check username and password.")
        except paramiko.SSHException as e:
            self.output_text.insert(tk.END, f"Error during SSH connection: {str(e)}")
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
        host_to_ping = "8.8.8.8"  # Change to your desired host
        self.run_command(f"/ping {host_to_ping}")

    def toggle_safe_mode(self):
        self.run_command("/ip firewall set safe-mode=no")

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
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the MikroTik Router
            ssh.connect(router_ip, port=ssh_port, username="admin", password="your_password")

            # Run the specified command
            stdin, stdout, stderr = ssh.exec_command(command)

            # Display the output
            output = stdout.read().decode("utf-8")
            self.output_text.insert(tk.END, output)

            # Close the SSH connection
            ssh.close()

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MikroTikManager(root)
    root.mainloop()
