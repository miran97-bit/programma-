import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Funzioni di calcolo
def calculate_delta_l(m, a, T0, T0_prime, E, S):
    constant = 0.98
    term1 = ((constant * m) ** 2 * a ** 3) / 24
    term2 = (1 / T0 ** 2) - (1 / T0_prime ** 2)
    term3 = (T0_prime - T0) * a / (E * S)
    delta_l = term1 * term2 + term3
    return delta_l

def find_best_T0_prime(m, a, T0, E, S, target_delta_l, T0_prime_start, T0_prime_end, step):
    best_T0_prime = None
    smallest_difference = float('inf')
    
    T0_prime = T0_prime_start
    while T0_prime <= T0_prime_end:
        delta_l = calculate_delta_l(m, a, T0, T0_prime, E, S)
        difference = abs(delta_l - target_delta_l)
        
        if difference < smallest_difference:
            smallest_difference = difference
            best_T0_prime = T0_prime
        
        T0_prime += step
    
    return best_T0_prime

def load_csv():
    try:
        global df
        df = pd.read_csv('dati_input.csv')
        menu_options = df['ID'].tolist()
        for dropdown in dropdowns:
            menu = dropdown['menu']
            menu.delete(0, 'end')
            for row_id in menu_options:
                menu.add_command(label=row_id, command=tk._setit(selected_id, row_id))
        messagebox.showinfo("Success", "CSV file loaded successfully. Please select an ID.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file: {e}")

def on_select(*args):
    try:
        row = df[df['ID'] == selected_id.get()]
        global m, E, S
        m = row['m'].values[0]
        E = row['E'].values[0]
        S = row['S'].values[0]
        messagebox.showinfo("Success", f"Selected ID: {selected_id.get()}\nm: {m}, E: {E}, S: {S}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set values from selection: {e}")

# Funzione di calcolo per la prima scheda
def calculate_tab1():
    try:
        Q1 = float(entry_Q1.get())
        Q2 = float(entry_Q2.get())
        Q3 = float(entry_Q3.get())
        a1 = float(entry_a1.get())
        a2 = float(entry_a2.get())
        T0 = float(entry_T0_tab1.get())

        # Calcoli
        h1 = Q2 - Q1
        h2 = Q2 - Q3
        global P
        P = ((a1 + a2) / 2) * 0.98 * m + T0 * (h1 / a1 + h2 / a2)

        # Messaggio di avviso con il valore di P
        messagebox.showinfo("Risultato", f"Il valore P è: {P}")
    except ValueError:
        messagebox.showerror("Error", "Inserisci valori numerici validi in tutte le caselle.")

# Funzione per generare PDF in base ai valori di input e al risultato
def generate_pdf():
    try:
        Q1 = entry_Q1.get()
        Q2 = entry_Q2.get()
        Q3 = entry_Q3.get()
        a1 = entry_a1.get()
        a2 = entry_a2.get()
        T0 = entry_T0_tab1.get()

        # Creazione del file PDF
        c = canvas.Canvas("calcolo_tab1.pdf", pagesize=A4)
        c.drawString(100, 800, "Risultati Calcolo Scheda 1")
        c.drawString(100, 780, f"ID Selezionato: {selected_id.get()}")
        c.drawString(100, 760, f"Q1: {Q1}")
        c.drawString(100, 740, f"Q2: {Q2}")
        c.drawString(100, 720, f"Q3: {Q3}")
        c.drawString(100, 700, f"a1: {a1}")
        c.drawString(100, 680, f"a2: {a2}")
        c.drawString(100, 660, f"T0: {T0}")
        c.drawString(100, 640, f"m: {m}")
        c.drawString(100, 620, f"Valore di P: {P}")

        # Salva il PDF
        c.save()
        messagebox.showinfo("PDF Generato", "Il calcolo è stato salvato in 'calcolo_tab1.pdf'")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la generazione del PDF: {e}")

# Funzione di calcolo per la quarta scheda
def calculate_tab4():
    try:
        a = float(entry_a.get())
        T0 = float(entry_T0_tab4.get())
        target_delta_l = float(entry_delta_l.get())
        
        T0_prime_start = 30
        T0_prime_end = 1500
        step = 1
        
        best_T0_prime = find_best_T0_prime(m, a, T0, E, S, target_delta_l, T0_prime_start, T0_prime_end, step)
        messagebox.showinfo("Result", f"The optimal value of T0_prime is: {best_T0_prime}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for a, T0, and delta_l")

# Creazione della GUI
root = tk.Tk()
root.title("Calcolatore Delta L")

notebook = ttk.Notebook(root)

# Variabile per tracciare la selezione dell'ID
selected_id = tk.StringVar()
selected_id.trace("w", on_select)
dropdowns = []

# Scheda 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Scheda 1")

tab1_entries = []
entry_names = ["Q1", "Q2", "Q3", "a1", "a2", "T0"]
entries = {}

# Creazione delle caselle di input per Scheda 1
for i, name in enumerate(entry_names):
    tk.Label(tab1, text=name).grid(row=i, column=0)
    entry = tk.Entry(tab1)
    entry.grid(row=i, column=1)
    entries[name] = entry  # Salva le caselle di input per riferimento
    tab1_entries.append(entry)

# Assegnazione delle variabili di input per Q1, Q2, Q3, a1, a2 e T0 nella prima scheda
entry_Q1 = entries["Q1"]
entry_Q2 = entries["Q2"]
entry_Q3 = entries["Q3"]
entry_a1 = entries["a1"]
entry_a2 = entries["a2"]
entry_T0_tab1 = entries["T0"]

# Dropdown per ID in Scheda 1
dropdown_tab1 = tk.OptionMenu(tab1, selected_id, ())
dropdown_tab1.grid(row=0, column=2)
dropdowns.append(dropdown_tab1)

# Pulsanti calcola ed estrai per Scheda 1
tk.Button(tab1, text="Calcola", command=calculate_tab1).grid(row=7, column=0, columnspan=2)
tk.Button(tab1, text="Estrai", command=generate_pdf).grid(row=7, column=2)

# Scheda 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Scheda 2")
dropdown_tab2 = tk.OptionMenu(tab2, selected_id, ())
dropdown_tab2.grid(row=0, column=0)
dropdowns.append(dropdown_tab2)

# Scheda 3
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Scheda 3")
dropdown_tab3 = tk.OptionMenu(tab3, selected_id, ())
dropdown_tab3.grid(row=0, column=0)
dropdowns.append(dropdown_tab3)

# Scheda 4
tab4 = ttk.Frame(notebook)
notebook.add(tab4, text="Scheda 4")

tk.Label(tab4, text="a").grid(row=0, column=0)
entry_a = tk.Entry(tab4)
entry_a.grid(row=0, column=1)

tk.Label(tab4, text="T0").grid(row=1, column=0)
entry_T0_tab4 = tk.Entry(tab4)
entry_T0_tab4.grid(row=1, column=2)

tk.Label(tab4, text="delta_l").grid(row=2, column=0)
entry_delta_l = tk.Entry(tab4)
entry_delta_l.grid(row=2, column=1)

# Dropdown per ID in Scheda 4
dropdown_tab4 = tk.OptionMenu(tab4, selected_id, ())
dropdown_tab4.grid(row=0, column=2)
dropdowns.append(dropdown_tab4)

# Pulsante calcola per Scheda 4
tk.Button(tab4, text="Calcola", command=calculate_tab4).grid(row=3, column=0, columnspan=2)

# Caricamento CSV all'avvio
load_csv()

notebook.pack(expand=True, fill="both")
root.mainloop()
