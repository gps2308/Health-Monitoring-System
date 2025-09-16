import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# API URL
API_URL = "https://fj4emwodxk.execute-api.us-east-1.amazonaws.com/health"

# Function to analyze and give instructions
def analyze_data(hr, spo2, temp):
    instructions = []

    # Heart Rate Analysis
    try:
        hr = float(hr)
        if hr < 60:
            instructions.append("⚠️ Heart Rate Low: May indicate bradycardia. Consult a doctor if persistent.")
        elif hr > 100:
            instructions.append("⚠️ Heart Rate High: Could indicate tachycardia. Take rest, consult if needed.")
        else:
            instructions.append("✅ Heart Rate Normal")
    except:
        instructions.append("❓ Heart Rate Data Not Available")

    # SpO₂ Analysis
    try:
        spo2 = float(spo2)
        if spo2 < 90:
            instructions.append("🚨 SpO₂ Very Low: Seek medical attention immediately!")
        elif spo2 < 95:
            instructions.append("⚠️ SpO₂ Slightly Low: Practice deep breathing, monitor closely.")
        else:
            instructions.append("✅ SpO₂ Normal")
    except:
        instructions.append("❓ SpO₂ Data Not Available")

    # Temperature Analysis
    try:
        temp = float(temp)
        if temp < 97:
            instructions.append("⚠️ Temperature Low: May indicate hypothermia. Keep warm.")
        elif temp > 100.4:
            instructions.append("🚨 Fever Detected: Stay hydrated, consult a doctor if high or persistent.")
        else:
            instructions.append("✅ Temperature Normal")
    except:
        instructions.append("❓ Temperature Data Not Available")

    return "\n".join(instructions)

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
            instruction_box.config(text="No data available.")
        else:
            hr = data.get("Heart rate", "N/A")
            sp = data.get("Spo2", "N/A")
            tp = data.get("Temperature", "N/A")

            heart_value.config(text=hr)
            spo2_value.config(text=sp)
            temp_value.config(text=tp)

            # Analyze and display instructions
            instructions = analyze_data(hr, sp, tp)
            instruction_box.config(text=instructions)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("HTTP Error", f"Error fetching data:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

# Create main window
root = tk.Tk()
root.title("Smart Health Dashboard")
root.geometry("600x600")
root.configure(bg="#f0f8ff")

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

# Load icons
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

# SpO₂
tk.Label(data_frame, image=spo2_icon, bg="#f0f8ff").grid(row=0, column=1, padx=10, pady=5)
spo2_value = tk.Label(data_frame, text="N/A", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="green")
spo2_value.grid(row=1, column=1)

# Temperature
tk.Label(data_frame, image=temp_icon, bg="#f0f8ff").grid(row=0, column=2, padx=10, pady=5)
temp_value = tk.Label(data_frame, text="N/A", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="orange")
temp_value.grid(row=1, column=2)

# Instruction Box
instruction_box = tk.Label(root, text="Instructions will appear here.", wraplength=500, justify="left",
                           font=("Arial", 12), bg="#f0f8ff", fg="black")
instruction_box.pack(pady=20)

# Run GUI
root.mainloop()
