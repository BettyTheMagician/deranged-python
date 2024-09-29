#!/usr/bin/env python3
import tkinter as tk 
from tkinter import PhotoImage
import csv 
import requests

#----------Constants and methods-------------#
url = 'https://api.humpool.com/v1/assets/balance'
TOKEN = 'EnterYOURToken'

file_path = "make/a/csv/file/path"

# Function to make an API request
def main_request(mining_user_name, currency):
    headers = {
        'Content-Type': 'application/json',
        'HPP-API-SECRET': TOKEN,
    }
    
    payload = {
        'currency': currency,
        'mining_user_name': mining_user_name
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload)  # using requests directly
        r.raise_for_status()  # Raises an error for 4xx and 5xx responses
        return r.json()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP Error: {http_err}, Response: {r.text if r else 'No response'}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Error: {str(e)}"}

# Function to save data to a CSV file
def save_to_csv(data):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data.get('balance', 'N/A'), data.get('paid', 'N/A'), data.get('total_income', 'N/A')])  # Adjust as needed

# Function to show balance and handle Tkinter integration
def show_balance(entry_username, entry_currency, balance_label):
    mining_user_name = entry_username.get()
    currency = entry_currency.get()
    
    response_data = main_request(mining_user_name, currency)
    
    if "error" in response_data:
        balance_label.config(text=f"Error: {response_data['error']}")
    else:
        balance_info = response_data.get('balance_info', {})
        balance_label.config(text=f"Balance: {balance_info.get('balance', 'N/A')}")
        save_to_csv(balance_info)

# Tkinter setup
def setup_gui():
    root = tk.Tk()
    root.title("rigWatcher")
    root.iconphoto(False, tk.PhotoImage(file='enchantedpick.png'))
    # Labels and entry fields
    tk.Label(root, text="Mining Username:").grid(row=0, column=0, padx=10, pady=10)
    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Currency:").grid(row=1, column=0, padx=10, pady=10)
    entry_currency = tk.Entry(root)
    entry_currency.grid(row=1, column=1, padx=10, pady=10)

    # Button to check balance
    balance_label = tk.Label(root, text="")
    balance_label.grid(row=3, columnspan=2, padx=10, pady=10)

    check_button = tk.Button(root, text="Check Balance", command=lambda: show_balance(entry_username, entry_currency, balance_label))
    check_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI setup
if __name__ == "__main__":
    setup_gui()
