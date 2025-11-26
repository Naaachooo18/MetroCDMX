import tkinter as tk
from Interfaz import InterfazMetro2025

def main():
    """
    Punto de entrada de la 
    Configura el entorno gráfico y lanza la vent
    """
    try:
        from ctypes import windll                   # Bloque especifico para Windows para que las aplicaciones
        windll.shcore.SetProcessDpiAwareness(1)     # de tKinter no se vean borrosas
    except:                                         
        pass                                        # Si no estamos en windows, no hace nada

    root = tk.Tk()                                  # Creamos la ventana principal
    
    
    app = InterfazMetro2025(root)                   # Carga la informacion de la interfaz y lo dibuja
    
    # Bucle para mantener la ventana abierta, el programa no pasa de esta linea hasta
    # que se cierre la ventana
    root.mainloop()

if __name__ == "__main__":
    main()
    