import csv
import tkinter as tk
import os
import datetime
import pymysql
from sshtunnel import SSHTunnelForwarder

# Database and SSH configurations
db_config = {
    "host": "159.203.140.48",
    "user": "fireworks",
    "password": "fireworks",
    "database": "fireworks"
}
ssh_host = '159.203.140.48'
ssh_port = 22
ssh_username = 'WillCall'
ssh_private_key = os.path.join(os.path.expanduser("~"), "Desktop", "id_rsa_fireworks.key")
mysql_host = '127.0.0.1'
mysql_port = 3306
mysql_user = 'fireworks'
mysql_password = 'fireworks'
mysql_db = 'fireworks'

def fetch_data_from_db():
    try:
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_pkey=ssh_private_key,
            remote_bind_address=(mysql_host, mysql_port)
        ) as tunnel:
            print("SSH Tunnel is open.")
            connection = pymysql.connect(
                host='127.0.0.1',
                port=tunnel.local_bind_port,
                user=mysql_user,
                password=mysql_password,
                database=mysql_db
            )
            cursor = connection.cursor()
            cursor.execute("SELECT orderID, fullname, generalPermitQuantity, additionalgeneralPermitQuantity, premiumPermitQuantity, adultWristbandQuantity, youthWristbandQuantity, dayOfAttend FROM Orders")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            
            file_path = os.path.join(os.path.expanduser("~"), "Desktop", "Tickets.csv")
            
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)  # Write headers
                writer.writerows(rows)  # Write data rows
            
            print(f"Success! Data exported to {file_path}")
            cursor.close()
            connection.close()
    except:
        print("Failed to connect to database. Proceeding with existing Tickets.csv file.")

def validateOrderNumber():
    # Order ID from GUI
    orderID = entry.get().strip()
    name = ""
    generalParking = 0
    additionalParking = 0
    premiumParking = 0
    adultWristband = 0
    youthWristband = 0
    validity = "NOT VALID"
    found = False
    notValid = True
    x = datetime.datetime.today()

    # Locate CSV file in the user's Downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Desktop")
    csv_file_path = os.path.join(downloads_folder, 'Tickets.csv')

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        result_label.config(text="ERROR: Tickets.csv not found in Desktop", fg="red")
        result_label.pack(pady=10)
        name_label.pack_forget()
        generalParking_label.pack_forget()
        premiumParking_label.pack_forget()
        adultWristband_label.pack_forget()
        youthWristband_label.pack_forget()
        ticket_not_found_label.pack_forget()
        entry.delete(0, tk.END)
        return

    # Read CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip CSV header
        for lines in reader:
            csvOrderID = lines[0]
            if orderID == csvOrderID:
                name = lines[1].upper()
                generalParking = lines[2]
                additionalParking = lines[3]
                premiumParking = lines[4]
                adultWristband = lines[5]
                youthWristband = lines[6]
                dayOfEvent = lines[7]
                found = True
                break

    # Ticket not found
    if not found:
        validity = "NOT VALID: NOT FOUND"
        result_label.pack(pady=10)
        ticket_not_found_label.pack(pady=20)
        name_label.pack_forget()
        generalParking_label.pack_forget()
        premiumParking_label.pack_forget()
        adultWristband_label.pack_forget()
        youthWristband_label.pack_forget()
    else:
        todayDate = x.strftime('%Y-%m-%d')
        print(todayDate)
        print(dayOfEvent)
        if todayDate == dayOfEvent:
            validity = "VALID"
            notValid = False
        else:
            validity = "NOT VALID: INCORRECT DATE"
            notValid = True
        ticket_not_found_label.pack_forget()

        # Pass back values
        name_label.config(text=f"NAME: {name}", fg="black")
        generalParking_label.config(text=f"GENERAL PARKING PASS: {int(generalParking) + int(additionalParking)}", fg="black")
        premiumParking_label.config(text=f"PREMIUM PARKING PASS: {premiumParking}", fg="black")
        adultWristband_label.config(text=f"ADULT WRISTBAND: {adultWristband}", fg="black")
        youthWristband_label.config(text=f"YOUTH WRISTBAND: {youthWristband}", fg="black")

        result_label.pack(pady=10)
        name_label.pack(pady=20)
        generalParking_label.pack(pady=20)
        premiumParking_label.pack(pady=20)
        adultWristband_label.pack(pady=20)
        youthWristband_label.pack(pady=20)

    result_label.config(text=f"{validity}", fg="green" if not notValid else "red")
    entry.delete(0, tk.END)

fetch_data_from_db()

root = tk.Tk()
root.title("Hagley Ticket Validator")
root.configure(bg='#D9D9D9')
root.update_idletasks()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Input Frame
input_frame = tk.Frame(root, bg='#D9D9D9')
input_frame.pack(pady=20)

# Entry Box
entry_label = tk.Label(input_frame, text="Enter Order Number:", fg="black", bg="#D9D9D9", font=("Lato", 40))
entry_label.pack(side="left", padx=10)

entry = tk.Entry(input_frame, font=("Lato", 40), width=20)
entry.pack(side="left", padx=10)

# Submit Button
validate_button = tk.Button(input_frame, fg="white", bg="#02435F", text="SUBMIT", font=("Lato", 30), command=validateOrderNumber)
validate_button.pack(side="left", padx=10)

# Labels
result_label = tk.Label(root, text="VALID:", fg="black", bg="#D9D9D9", font=("Lato", 60))
name_label = tk.Label(root, text="NAME: ", fg="black", bg="#D9D9D9", font=("Lato", 50))
generalParking_label = tk.Label(root, text="GENERAL PARKING PASS: ", fg="black", bg="#D9D9D9", font=("Lato", 50))
premiumParking_label = tk.Label(root, text="PREMIUM PARKING PASS: ", fg="black", bg="#D9D9D9", font=("Lato", 50))
adultWristband_label = tk.Label(root, text="ADULT WRISTBAND: ", fg="black", bg="#D9D9D9", font=("Lato", 50))
youthWristband_label = tk.Label(root, text="YOUTH WRISTBAND: ", fg="black", bg="#D9D9D9", font=("Lato", 50))
ticket_not_found_label = tk.Label(root, text="TICKET NOT FOUND", fg="red", bg="#D9D9D9", font=("Lato", 60))

# Bind the Enter key (both regular and number pad) to the validateOrderNumber function
root.bind('<Return>', lambda event: validateOrderNumber())

# Run GUI
root.mainloop()
