import tkinter as tk
from tkinter import ttk
from Visualizer_Utils.gui_funcs import load_all_files, hex_to_bin

class RiscVGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Visualizador RiscV')
        self.instruction_memory, self.assembly_code, self.data_memory, self.dump_registers = load_all_files()

        # Frame para registros
        self.frame1 = ttk.LabelFrame(root, text="Registros")
        self.frame1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree1 = ttk.Treeview(self.frame1)
        self.tree1["columns"] = ("Registro", "Valor")
        self.tree1.column("#0", width=0, stretch=tk.NO)
        self.tree1.column("Registro", anchor=tk.W, width=300)
        self.tree1.column("Valor", anchor=tk.W, width=300)

        self.tree1.heading("#0", text="", anchor=tk.W)
        self.tree1.heading("Registro", text="Registro", anchor=tk.W)
        self.tree1.heading("Valor", text="Valor", anchor=tk.W)
        self.tree1.pack()

        # Frame para el programa en assembly
        self.frame2 = ttk.LabelFrame(root, text="Programa")
        self.frame2.grid(row=0, column=0, padx=10, pady=10)
        self.text2 = tk.Text(self.frame2, height=15, width=80)
        self.text2.pack()
        self.text2.insert(tk.END, "".join(self.assembly_code))

        # Frame para memoria
        self.frame3 = ttk.LabelFrame(root, text="Memoria")
        self.frame3.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tree3 = ttk.Treeview(self.frame3)
        self.tree3["columns"] = ("Byte", "Valor")
        self.tree3.column("#0", width=0, stretch=tk.NO)
        self.tree3.column("Byte", anchor=tk.W, width=300)
        self.tree3.column("Valor", anchor=tk.W, width=300)

        self.tree3.heading("#0", text="", anchor=tk.W)
        self.tree3.heading("Byte", text="Byte", anchor=tk.W)
        self.tree3.heading("Valor", text="Valor", anchor=tk.W)
        self.tree3.pack()

        # Combobox para seleccionar la vista del programa
        opciones_menu = ['Assembly', 'Binario', 'Hex']
        self.opcion = tk.StringVar()
        self.opcion.set('Assembly')
        self.menu = ttk.Combobox(self.frame2, textvariable=self.opcion, values=opciones_menu)
        self.menu.bind("<<ComboboxSelected>>", lambda event: self.update_program_view())
        self.menu.pack()

        # Combobox para seleccionar la vista de los registros
        opciones_registros = ['Hex', 'Binario', 'Decimal', 'Decimal Signed']
        self.opcion_reg = tk.StringVar()
        self.opcion_reg.set('Hex')
        self.menu_reg = ttk.Combobox(self.frame1, textvariable=self.opcion_reg, values=opciones_registros)
        self.menu_reg.bind("<<ComboboxSelected>>", lambda event: self.update_register_view())
        self.menu_reg.pack()

        # Combobox para seleccionar la vista de la memoria
        opciones_memoria = ['Hex', 'Binario', 'Decimal', 'Decimal Signed']
        self.opcion_mem = tk.StringVar()
        self.opcion_mem.set('Hex')
        self.menu_mem = ttk.Combobox(self.frame3, textvariable=self.opcion_mem, values=opciones_memoria)
        self.menu_mem.bind("<<ComboboxSelected>>", lambda event: self.update_memory_view())
        self.menu_mem.pack()

        self.update_ui()
    
    # Funciones para actualizar los widgets con los datos cargados
    def update_program_view(self):
        current_option = self.opcion.get()
        if current_option == 'Assembly':
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, "".join(self.assembly_code))
        elif current_option == 'Hex':
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, "".join(self.instruction_memory))
        elif current_option == 'Binario':
            self.text2.delete(1.0, tk.END)
            bin_representation = [hex_to_bin(line.strip()) + '\n' for line in self.instruction_memory]
            self.text2.insert(tk.END, "".join(bin_representation))

    # Funciones para actualizar los widgets con los datos cargados
    def update_register_view(self):
        current_option = self.opcion_reg.get()
        self.tree1.delete(*self.tree1.get_children())
        for i, val in enumerate(self.dump_registers):
            if current_option == 'Hex':
                self.tree1.insert(parent='', index='end', iid=i, values=(f"x{i}", val.strip()))
            elif current_option == 'Binario':
                self.tree1.insert(parent='', index='end', iid=i, values=(f"x{i}", hex_to_bin(val.strip())))
            elif current_option == 'Decimal':
                self.tree1.insert(parent='', index='end', iid=i, values=(f"x{i}", int(val.strip(), 16)))
            elif current_option == 'Decimal Signed':
                # Convirtiendo el hexadecimal a decimal signed
                decimal_val = int(val.strip(), 16)
                if decimal_val >= 2**(len(val.strip())*4 - 1):
                    decimal_val -= 2**(len(val.strip())*4)
                self.tree1.insert(parent='', index='end', iid=i, values=(f"x{i}", decimal_val))

    def update_memory_view(self):
        current_option = self.opcion_mem.get()
        self.tree3.delete(*self.tree3.get_children())
        for i, val in enumerate(self.data_memory):
            if current_option == 'Hex':
                self.tree3.insert(parent='', index='end', iid=i, values=(f"{i}", val.strip()))
            elif current_option == 'Binario':
                self.tree3.insert(parent='', index='end', iid=i, values=(f"{i}", hex_to_bin(val.strip())))
            elif current_option == 'Decimal':
                self.tree3.insert(parent='', index='end', iid=i, values=(f"{i}", int(val.strip(), 16)))
            elif current_option == 'Decimal Signed':
                # Convirtiendo el hexadecimal a decimal signed
                decimal_val = int(val.strip(), 16)
                if decimal_val >= 2**(len(val.strip())*4 - 1):
                    decimal_val -= 2**(len(val.strip())*4)
                self.tree3.insert(parent='', index='end', iid=i, values=(f"{i}", decimal_val))
            
    def update_program_view(self):
        current_option = self.opcion.get()
        if current_option == 'Assembly':
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, "".join(self.assembly_code))
        elif current_option == 'Hex':
            self.text2.delete(1.0, tk.END)
            self.text2.insert(tk.END, "".join(self.instruction_memory))
        elif current_option == 'Binario':
            self.text2.delete(1.0, tk.END)
            bin_representation = [hex_to_bin(line.strip()) + '\n' for line in self.instruction_memory]
            self.text2.insert(tk.END, "".join(bin_representation))

    def update_ui(self):
        self.update_program_view()
        self.update_register_view()
        self.update_memory_view()

    def run(self):
        self.root.mainloop()