from Visualizer_Utils.gui_class import RiscVGUI
import tkinter as tk

def run_program():
    root = tk.Tk()
    app = RiscVGUI(root=root)
    app.run()

if __name__ == '__main__':
    run_program()