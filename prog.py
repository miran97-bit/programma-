import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def calculate_delta_l(m, a, T0, T0_prime, E, S):
    constant = 0.98
    term1 = ((constant * m) ** 2 * a ** 3) / 24
    term2 = (1 / T0 ** 2) - (1 / T0_prime ** 2)
    term3 = (T0_prime - T0) * a / (E * S)
    delta_l = term1 * term2 + term3
    return delta_l

def generate_pdf():
    try:
        Q1 = float(entry_Q1.get())
        Q2 = float(entry_Q2.get())
        Q3 = float(entry_Q3.get())
        a1 = float(entry_a1.get())
        a2 = float(entry_a2.get())
        T0 = float(entry_T0_tab1.get())
        
        h1 = Q2 - Q1
        h2 = Q2 - Q3
        P = ((a1 + a2) / 2) * 0.98 * m + T0 * (h1 / a1 + h2 / a2)
        
        c = canvas.Canvas("calcolo_AS.pdf", pagesize=A4)
        c.drawString(100, 800, "Risultati Calcolo AS")
        c.drawString(100, 780, f"ID Selezionato: {selected_id.get()}")
        c.drawString(100, 760, f"Q1: {Q1}, Q2: {Q2}, Q3: {Q3}")
        c.drawString(100, 740, f"a1: {a1}, a2: {a2}, T0: {T0}")
        c.drawString(100, 720, f"m: {m}")
        
        formula = "P = ((a1 + a2) / 2) * 0.98 * m + T0 * (h1 / a1 + h2 / a2)"
        c.drawString(100, 700, "Formula usata:")
        c.drawString(100, 680, formula)
        c.drawString(100, 660, f"Con valori: P = (({a1} + {a2}) / 2) * 0.98 * {m} + {T0} * ({h1} / {a1} + {h2} / {a2})")
        c.drawString(100, 640, f"Risultato P: {P}")
        
        c.save()
        messagebox.showinfo("PDF Generato", "Il calcolo è stato salvato in 'calcolo_AS.pdf'")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante la generazione del PDF: {e}")

root = tk.Tk()
root.title("Calcolatore Delta L")
notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="AS")

tab1_entries = []
entry_names = ["Q1", "Q2", "Q3", "a1", "a2", "T0"]
entries = {}

for i, name in enumerate(entry_names):
    tk.Label(tab1, text=name).grid(row=i, column=0)
    entry = tk.Entry(tab1)
    entry.grid(row=i, column=1)
    entries[name] = entry
    tab1_entries.append(entry)

entry_Q1 = entries["Q1"]
entry_Q2 = entries["Q2"]
entry_Q3 = entries["Q3"]
entry_a1 = entries["a1"]
entry_a2 = entries["a2"]
entry_T0_tab1 = entries["T0"]

tk.Button(tab1, text="Estrai", command=generate_pdf).grid(row=7, column=2)

notebook.pack(expand=True, fill="both")
root.mainloop()

