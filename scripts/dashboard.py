import tkinter as tk
from tkinter import messagebox  # <-- ESTO es lo que probablemente faltaba
import os
import subprocess
import socket

class RPiDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Stream")
        
        # Modo pantalla completa
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg='#1e1e2e')

        # Estilos
        btn_style = {"font": ("Arial", 12, "bold"), "fg": "white", "height": 2}
        
        # Botón de Salida (X)
        self.btn_exit = tk.Button(root, text="X", bg='#45475a', fg='white', 
                                 command=self.root.destroy, font=("Arial", 10, "bold"), bd=0)
        self.btn_exit.place(x=440, y=5, width=30, height=30)

        # IP y Temperatura
        self.info_label = tk.Label(root, text="Buscando IP...", font=("Arial", 10), bg='#1e1e2e', fg='#a6adc8')
        self.info_label.pack(pady=(20, 5))

        self.temp_label = tk.Label(root, text="TEMP: --°C", font=("Arial", 22, "bold"), bg='#1e1e2e', fg='#f38ba8')
        self.temp_label.pack(pady=10)

        self.status_label = tk.Label(root, text="STREAM: VERIFICANDO", font=("Arial", 12), bg='#1e1e2e', fg='#f9e2af')
        self.status_label.pack(pady=5)

        # Botón Stream
        self.btn_stream = tk.Button(root, text="INICIAR / DETENER STREAM", bg='#89b4fa', **btn_style, command=self.toggle_stream)
        self.btn_stream.pack(fill='x', padx=50, pady=10)

        # Botón Apagar
        self.btn_off = tk.Button(root, text="APAGAR RASPBERRY", bg='#f38ba8', **btn_style, command=self.shutdown_pi)
        self.btn_off.pack(fill='x', padx=50, pady=10)

        self.update_stats()

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "Desconectado"

    def update_stats(self):
        try:
            temp = os.popen("vcgencmd measure_temp").readline().replace("temp=","").strip()
            self.temp_label.config(text=f"TEMP: {temp}")
            self.info_label.config(text=f"IP: {self.get_ip()}")

            status = subprocess.run(['systemctl', 'is-active', 'stream_obs.service'], capture_output=True, text=True).stdout.strip()
            if status == "active":
                self.status_label.config(text="● EN VIVO (SRT)", fg='#a6e3a1')
            else:
                self.status_label.config(text="○ DETENIDO", fg='#f38ba8')
        except:
            pass # Evita que el programa se cierre si hay un error de lectura

        self.root.after(3000, self.update_stats)

    def toggle_stream(self):
        status = subprocess.run(['systemctl', 'is-active', 'stream_obs.service'], capture_output=True, text=True).stdout.strip()
        action = "stop" if status == "active" else "start"
        subprocess.run(['sudo', 'systemctl', action, 'stream_obs.service'])

    def shutdown_pi(self):
        # Usamos messagebox de forma segura
        if messagebox.askokcancel("Confirmar", "¿Deseas apagar la Raspberry Pi?"):
            os.system("sudo shutdown -h now")

if __name__ == "__main__":
    root = tk.Tk()
    app = RPiDashboard(root)
    root.mainloop()