import tkinter as tk
from InterfazModerna import InterfazMetro2025

def main():
    # Configuración para pantallas de alta resolución (DPI Awareness)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

    root = tk.Tk()
    
    # Aquí inicializamos la interfaz moderna
    app = InterfazMetro2025(root)
    
    # Bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()