import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# API URL
API_URL = "https://fj4emwodxk.execute-api.us-east-1.amazonaws.com/health"

# Fetch health data from API
def fetch_data():
    deviceid = device_entry.get().strip()
    timestamp = timestamp_entry.get().strip()

    if not deviceid or not timestamp:
        messagebox.showwarning("Input Error", "Please enter both Device ID and Timestamp.")
        return

    try:
        response = requests.get(API_URL, params={"deviceid": deviceid, "timestamp": timestamp})
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            messagebox.showerror("API Error", data["error"])
            heart_value.config(text="N/A")
            spo2_value.config(text="N/A")
            temp_value.config(text="N/A")
        else:
            heart_value.config(text=data.get("Heart rate", "N/A"))
            spo2_value.config(text=data.get("Spo2", "N/A"))
            temp_value.config(text=data.get("Temperature", "N/A"))

    except requests.exceptions.RequestException as e:
        messagebox.showerror("HTTP Error", f"Error fetching data:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

# Create main window
root = tk.Tk()
root.title("Smart Health Dashboard")
root.geometry("500x500")
root.configure(bg="#f0f8ff")  # light blue background

# Title
title = tk.Label(root, text="Health Monitoring Dashboard", font=("Helvetica", 18, "bold"), bg="#f0f8ff")
title.pack(pady=10)

# Input frame
input_frame = tk.Frame(root, bg="#f0f8ff")
input_frame.pack(pady=5)

tk.Label(input_frame, text="Device ID:", bg="#f0f8ff", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
device_entry = tk.Entry(input_frame, width=25, font=("Arial", 12))
device_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Timestamp:", bg="#f0f8ff", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
timestamp_entry = tk.Entry(input_frame, width=25, font=("Arial", 12))
timestamp_entry.grid(row=1, column=1, padx=5, pady=5)

fetch_btn = tk.Button(root, text="Fetch Data", command=fetch_data, bg="#00bfff", fg="white", font=("Arial", 12, "bold"))
fetch_btn.pack(pady=10)

# Data display frame
data_frame = tk.Frame(root, bg="#f0f8ff")
data_frame.pack(pady=10)

# Load icons (use raw strings for Windows paths)
heart_img = Image.open(r"C:\Users\GURPREET SINGH\OneDrive\Desktop\heart.png").resize((50,50))
heart_icon = ImageTk.PhotoImage(heart_img)

spo2_img = Image.open(r"C:\Users\GURPREET SINGH\OneDrive\Desktop\spo2.png").resize((50,50))
spo2_icon = ImageTk.PhotoImage(spo2_img)

temp_img = Image.open(r"C:\Users\GURPREET SINGH\OneDrive\Desktop\temperature.png").resize((50,50))
temp_icon = ImageTk.PhotoImage(temp_img)

# Heart Rate
tk.Label(data_frame, image=heart_icon, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5)
heart_value = tk.Label(data_frame, text="N/A", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="red")
heart_value.grid(row=1, column=0)

# SpO2
tk.Label(data_frame, image=spo2_icon, bg="#f0f8ff").grid(row=0, column=1, padx=10, pady=5)
spo2_value = tk.Label(data_frame, text="N/A", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="green")
spo2_value.grid(row=1, column=1)

# Temperature
tk.Label(data_frame, image=temp_icon, bg="#f0f8ff").grid(row=0, column=2, padx=10, pady=5)
temp_value = tk.Label(data_frame, text="N/A", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="orange")
temp_value.grid(row=1, column=2)

# Run GUI
root.mainloop()
