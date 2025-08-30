# Ecuacion de Vander Waals
# 
# P = nRT/(V-nb) - a*(n/V)2

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os, sys

# Función para acceder a archivos embebidos con PyInstaller
def resource_path(relative_path):
    """Devuelve la ruta absoluta de un recurso, funciona para dev y exe"""
    try:
        base_path = sys._MEIPASS  # carpeta temporal de PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Constante de los gases
valores_R = {
    "8.314 J/mol K": 8.314,
    "0.082 L atm/mol K":0.082,
}


#Cargar CSV
df = pd.read_csv(resource_path("gasess.csv"))

#Convertir a lista para usar en Tkinter
gases = df.set_index("Gas").to_dict(orient="index")
print(gases["Acetato de etilo"]) 

#Funciones
def presion_final():
    gas = combo_gas.get()
    R_key = combo_r.get()
    R = valores_R[R_key]



    if not gas:
        messagebox.showerror("Error", "Gas no encontrado en la lista")
        return
    
    try:
        n = float(entry_n.get())
        v = float(entry_v.get())
        t = float(entry_t.get())

        #Convertir volumen a Litros , SI ELIGE LA R con J la unidad de volumen debe estar en m3, sino en L
        if combo_vu.get() == "ml":
            v /=1000 
        #Convertir temperatura a Kelvin
        if combo_tu.get() == "°C":
            t+=273 

    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos")
        return

    a = gases[gas]["a (bar·L²/mol²)"]
    b = gases[gas]["b (L/mol)"]


    #Calculo para la presion segun la R seleccionada

    if "J/mol K" in R_key:

        if v-n*b <= 0:
            messagebox.showerror("Error", "Revise los datos ingresados!!")
            return
        #Volumen en m3
        v = v / 1000 # 1L = 0.001 m3
        b = b / 1000 # 1L/mol = 0.001 m3/mol

        #Convertir de bar L2/ mol2 a Pa m6/mol2
        #1 bar = 1e5 Pa, 1L2= 1x10-6 m6
        a = a * 0.1 

        #Presion Final:
        Presion = (n*R*t)/(v-n*b) - (a*(n**2)/(v**2))
        label_p.config(text=f"{Presion: .3e}")
        label_pu.config(text="Pa")

    
    else:

        if v-n*b <= 0:
            messagebox.showerror("Error", "Revise los datos ingresados!!")
            return

        a = a *0.98692 #(bar --> 0.98692 atm)

        Presion = (n*R*t)/(v-n*b) - (a*(n**2)/(v**2))
        label_p.config(text=f"{Presion: .3f}")
        label_pu.config(text="atm")


#Interfaz

ventana = tk.Tk()
ventana.title("CALCULADORA DE PRESION FINAL (VAN DER WAALS)")
ventana.geometry("550x300")
ventana.iconbitmap(resource_path("3327571.ico"))


#Menus Desplegables

#Lista de Gases
label_gas = tk.Label(ventana, text="Seleccione un gas: ")
label_gas.grid(row=0, column=0, pady=10, padx=20)
combo_gas = ttk.Combobox(ventana, values=list(gases.keys()), width=25)
combo_gas.grid(row=0, column=1, pady=10, padx=20)
combo_gas.current(0) #Selecciona al primero de la lista por defecto, en este caso CO2

#Selecciones el valor de R
label_r = tk.Label(ventana, text="Seleccione el valor de R que quiere utilizar: ")
label_r.grid(row=1, column=0, pady=10, padx=20)
combo_r = ttk.Combobox(ventana, values=list(valores_R.keys()), width=15)
combo_r.grid(row=1, column=1, pady=10, padx=20)
combo_r.current(0)

#Unidades de Temperatura
unidades_temp = ["K","°C"]
combo_tu = ttk.Combobox(ventana, values=unidades_temp, width=3)
combo_tu.grid(row=4, column=2, pady=5, padx=5)
combo_tu.current(0)
#Unidades de Volumen
unidades_vol = ["ml","L"]
combo_vu = ttk.Combobox(ventana, values=unidades_vol, width=3)
combo_vu.grid(row=3, column=2, pady=5, padx=5)
combo_vu.current(0)


#Entrada de datos
label_n = tk.Label(ventana, text="Ingrese el número de moles: ")
label_n.grid(row=2, column=0, pady=10, padx=20)
entry_n = tk.Entry(ventana)
entry_n.grid(row=2, column=1, pady=10, padx=20)

label_v = tk.Label(ventana,  text="Ingrese el volumen: ")
label_v.grid(row=3, column=0, pady=10, padx=20)
entry_v = tk.Entry(ventana)
entry_v.grid(row=3, column=1, pady=10, padx=20)

label_t = tk.Label(ventana,  text="Ingrese la temperatura: ")
label_t.grid(row=4, column=0, pady=10, padx=20)
entry_t = tk.Entry(ventana)
entry_t.grid(row=4, column=1, pady=10, padx=20)




#Boton para calcular
label_p = tk.Label(ventana, text="")
label_p.grid(row=5, column=1, pady=10, padx=50)

label_pu = tk.Label(ventana, text="")
label_pu.grid(row=5, column=2,pady=10, padx=10)

bnt = tk.Button(ventana, text="Calcular Presion", command=presion_final)
bnt.grid(row=5, column=0, pady=10, padx=50)

ventana.mainloop()

