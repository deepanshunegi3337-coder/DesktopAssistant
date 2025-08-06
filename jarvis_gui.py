import customtkinter as ctk
import json
import os
import threading
import psutil
import math
import time
import subprocess

STATUS_FILE = "jarvis_status.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisV4(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jarvis V4 Assistant")
        self.geometry("800x600")
        self.amplitude = 0

        self.status_label = ctk.CTkLabel(self, text="Starting...", font=("Arial", 18))
        self.status_label.pack(pady=10)

        self.canvas = ctk.CTkCanvas(self, width=200, height=200, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)
        self.animate_wave()

        self.stats_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.stats_label.pack(pady=5)
        self.update_stats()

        panel = ctk.CTkFrame(self)
        panel.pack(pady=10)
        for i, cmd in enumerate(["open chrome", "open notepad", "open youtube", "volume up", "volume down", "mute", "screenshot", "shutdown", "restart"]):
            ctk.CTkButton(panel, text=cmd.title(), command=lambda c=cmd: self.quick_command(c)).grid(row=i//3, column=i%3, padx=5, pady=5)

        threading.Thread(target=self.start_backend, daemon=True).start()
        self.update_gui()

    def start_backend(self):
        subprocess.Popen(["python", "jarvis_backend.py"])

    def quick_command(self, command):
        with open(STATUS_FILE, "w") as f:
            json.dump({"status": f"Quick command: {command}", "time": time.strftime("%H:%M:%S"), "amplitude": 0}, f)
        subprocess.Popen(["python", "jarvis_backend.py"])

    def animate_wave(self):
        self.canvas.delete("all")
        r = 50 + (self.amplitude / 200)
        self.canvas.create_oval(100 - r, 100 - r, 100 + r, 100 + r, outline="cyan", width=3)
        self.after(50, self.animate_wave)

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_status = f"{battery.percent}%" if battery else "N/A"
        self.stats_label.configure(text=f"CPU: {cpu}%  RAM: {ram}%  Battery: {battery_status}")
        self.after(2000, self.update_stats)

    def update_gui(self):
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r") as f:
                try:
                    status = json.load(f)
                    self.status_label.configure(text=f"Status: {status['status']} ({status['time']})")
                    self.amplitude = status.get("amplitude", 0)
                except:
                    pass
        self.after(1000, self.update_gui)

if __name__ == "__main__":
    app = JarvisV4()
    app.mainloop()
