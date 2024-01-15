import os
import shutil
import tkinter as tk
from tkinter import messagebox
from sys import exit
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
import pathlib


class MainGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.label_path = tk.Label(self.root, text="Path", font=('Arial', 13))
        self.label_path.pack(padx=10, pady=10)

        self.textbox_path = tk.Entry(self.root, font=('Arial', 13))
        self.textbox_path.pack(padx=10, pady=10)

        self.label_extensions = tk.Label(
            self.root, text="Extensions seperated by comma. Eg. png, jpg", font=('Arial', 13))
        self.label_extensions.pack(padx=10, pady=10)

        self.textbox_extensions = tk.Entry(self.root, font=('Arial', 13))
        self.textbox_extensions.pack(padx=10, pady=10)

        self.btn_backup = tk.Button(
            self.root, text="Create Backup", font=('Arial', 15), command=self.backup)
        self.btn_backup.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        if messagebox.askyesno(title="Quit", message="Do you really want to quit?"):
            self.root.destroy()

    def backup(self):
        entered_path = self.textbox_path.get()
        entered_extensions = self.textbox_extensions.get()
        extension_list = []
        is_path_ok = False
        is_extensions_ok = False

        if (entered_path and os.path.exists(entered_path) and os.path.isdir(entered_path)):
            print(f'Path {entered_path} OK')
            is_path_ok = True
        else:
            print('Invalid Path')

        if (entered_extensions):
            extension_list = entered_extensions.replace(" ", "").split(",")
            print(f'Extensions {extension_list} OK')
            is_extensions_ok = True
        else:
            print('Invalid Extensions')

        if (is_path_ok and is_extensions_ok):
            files = os.listdir(entered_path)
            now = datetime.now()
            dir_backup = f"{entered_path}/backup-{datetime.timestamp(now)}"
            os.makedirs(dir_backup)
            print(f"backingup at {dir_backup}")
            has_files = False
            zip_path = f"{dir_backup}.zip"
            folder_to_zip = pathlib.Path(dir_backup)

            for file in files:
                filename, extension = os.path.splitext(file)
                extension = extension[1:]
                if (extension in extension_list):
                    print(f"I need to backup {filename}")
                    from_file = f"{entered_path}/{file}"
                    to_file = f"{dir_backup}/{file}"
                    shutil.copyfile(from_file, to_file)
                    has_files = True

            if has_files:
                with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip:
                    for file in folder_to_zip.iterdir():
                        zip.write(file, arcname=file.name)
                        print(f"zipping {file}")

            messagebox.showinfo(
                title="Message", message=f"Backup Done at {entered_path}")
        else:
            messagebox.showinfo(
                title="Message", message=f"Invalid Path or Extensions")


MainGUI()
