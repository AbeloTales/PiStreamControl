import tkinter as tk
import os
import subprocess
import socket

class RPiDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Stream")
        self.root.geometry("480x320")
        self.root.configure(bg='#1e1e2e')

        # Estilos de botones y etiquetas
        btn_style = {"font": ("Arial", 12, "bold"), "fg": "white", "height": 2}
        
        # IP y Temperatura
        self.info_label = tk.Label(root, text="Iniciando...", font=("Arial", 10), bg='#1e1e2e', fg='#a6adc8')
        self.info_label.pack(pady=5)

        self.temp_label = tk.Label(root, text="TEMP: --°C", font=("Arial", 20, "bold"), bg='#1e1e2e', fg='#f38ba8')
        self.temp_label.pack(pady=10)

        # Estado del Stream
        self.status_label = tk.Label(root, text="STREAM: DESCONOCIDO", font=("Arial", 12), bg='#1e1e2e', fg='#f9e2af')
        self.status_label.pack(pady=5)

        # Botón Stream
        self.btn_stream = tk.Button(root, text="INICIAR / DETENER STREAM", bg='#89b4fa', **btn_style, command=self.toggle_stream)
        self.btn_stream.pack(fill='x', padx=40, pady=10)

        # Botón Apagar RPi
        self.btn_off = tk.Button(root, text="APAGAR RASPBERRY", bg='#f38ba8', **btn_style, command=self.shutdown_pi)
        self.btn_off.pack(fill='x', padx=40, pady=10)

        self.update_stats()

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "Sin Red"

    def update_stats(self):
        # Actualizar Temperatura
        temp = os.popen("vcgencmd measure_temp").readline().replace("temp=","").strip()
        self.temp_label.config(text=f"TEMP: {temp}")
        
        # Actualizar IP
        self.info_label.config(text=f"IP: {self.get_ip()}")

        # Actualizar Estado del Servicio
        status = subprocess.run(['systemctl', 'is-active', 'stream_obs.service'], capture_output=True, text=True).stdout.strip()
        if status == "active":
            self.status_label.config(text="● EN VIVO (SRT)", fg='#a6e3a1')
        else:
            self.status_label.config(text="○ DETENIDO", fg='#f38ba8')

        self.root.after(3000, self.update_stats)

    def toggle_stream(self):
        status = subprocess.run(['systemctl', 'is-active', 'stream_obs.service'], capture_output=True, text=True).stdout.strip()
        action = "stop" if status == "active" else "start"
        subprocess.run(['sudo', 'systemctl', action, 'stream_obs.service'])

    def shutdown_pi(self):
        if tk.messagebox.askokcancel("Apagar", "¿Seguro que quieres apagar la Pi?"):
            subprocess.run(['sudo', 'shutdown', '-h', 'now'])

if __name__ == "__main__":
    root = tk.Tk()
    # root.attributes('-fullscreen', True) # Descomenta esto cuando la pantalla esté lista
    app = RPiDashboard(root)
    root.mainloop()