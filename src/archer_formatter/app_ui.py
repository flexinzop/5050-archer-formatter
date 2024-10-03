import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import subprocess

# The graphical user interface script. It allows the user to select a CSV file and an output folder, and then convert the CSV file to XML.

def select_csv_file():
    global csv_file_path
    csv_file_path = filedialog.askopenfilename(
        title="Select CSV file", 
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if csv_file_path:
        csv_file_label.config(text=os.path.basename(csv_file_path))

def select_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory(title="Select Output Folder")
    if output_folder_path:
        output_folder_label.config(text=output_folder_path)

def convert_to_xml():
    if not csv_file_path or not output_folder_path:
        messagebox.showerror("Error", "Please select a CSV file and an output folder")
        return

    try:
        # @samuel Assuming main.py is conversion script
        subprocess.run(['python', 'main.py', csv_file_path, output_folder_path], check=True)
        messagebox.showinfo("Success", "Conversion completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")

# UI Setup
root = tk.Tk()
root.title("BACEN 5050 CSV-2-XML")

# App Title
title_label = tk.Label(root, text="BACEN 5050 CSV-2-XML", font=("Arial", 16))
title_label.pack(pady=10)

# CSV Input Button
csv_button = tk.Button(root, text="Input CSV File", command=select_csv_file)
csv_button.pack(pady=5)

# Display selected CSV file
csv_file_label = tk.Label(root, text="No file selected", font=("Arial", 10))
csv_file_label.pack(pady=5)

# Output Folder Button
output_button = tk.Button(root, text="Output Folder", command=select_output_folder)
output_button.pack(pady=5)

# Display selected output folder
output_folder_label = tk.Label(root, text="No folder selected", font=("Arial", 10))
output_folder_label.pack(pady=5)

# Convert Button
convert_button = tk.Button(root, text="Convert", command=convert_to_xml, bg="green", fg="white")
convert_button.pack(pady=20)

# Main loop
root.geometry("400x300")
root.mainloop()