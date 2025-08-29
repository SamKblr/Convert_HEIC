import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys


from src.functions import convert_HEIC_images_to_other_format_across_subfolders


class HEICConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("HEIC → PNG Converter")
        master.geometry("500x300")
        master.resizable(False, False)

        # Variables
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()

        # Widgets
        tk.Label(master, text="Source folder (HEIC):").pack(pady=(20, 5))
        tk.Entry(master, textvariable=self.source_dir, width=50).pack()
        tk.Button(master, text="Select…", command=self.choose_source_dir).pack(pady=5)

        tk.Label(master, text="Destination folder:").pack(pady=(20, 5))
        tk.Entry(master, textvariable=self.dest_dir, width=50).pack()
        tk.Button(master, text="Select…", command=self.choose_dest_dir).pack(pady=5)

        self.run_button = tk.Button(master, text="Run the conversion ", command=self.run_conversion)
        self.run_button.pack(pady=(30, 5))

        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack()

    def choose_source_dir(self):
        path = filedialog.askdirectory(title="Select the source folder (.HEIC)")
        if path:
            self.source_dir.set(path)

    def choose_dest_dir(self):
        path = filedialog.askdirectory(title="Select the destintion folder")
        if path:
            self.dest_dir.set(path)

    def run_conversion(self):
        src = self.source_dir.get()
        dst = self.dest_dir.get()

        if not src or not dst:
            messagebox.showerror("Error", "Select the two folders.")
            return

        if not os.path.exists(src):
            messagebox.showerror("Error", f"Invalid source folder : {src}")
            return

        if not os.path.exists(dst):
            messagebox.showerror("Error", f"Invalid destination folder : {dst}")
            return

        self.run_button.config(state="disabled")
        self.status_label.config(text="On going conversion…")

        # Lancer la conversion dans un thread pour ne pas bloquer la GUI
        threading.Thread(target=self.start_conversion, args=(src, dst), daemon=True).start()

    def start_conversion(self, src, dst):
        try:
            convert_HEIC_images_to_other_format_across_subfolders(
                src, dst, output_format="png", workers=4, overwrite=True
            )
            messagebox.showinfo("Sucess", "✅ Conversion finished !")
        except Exception as e:
            messagebox.showerror("Error", f"❌ An error occured :\n{e}")
        finally:
            self.status_label.config(text="")
            self.run_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = HEICConverterGUI(root)
    root.mainloop()
