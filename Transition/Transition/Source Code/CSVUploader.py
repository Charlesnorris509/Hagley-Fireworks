################################################################################################
# CSV Import Script for Hagley Fireworks Event
#
# Description:
# This script will process CSV files containing ticket orders for Hagley Museum and Library's 
# Annual Fireworks event. It will import that ticketing data into the 'Orders' table.
#
# Created by: Sarah Smith=
# Created on: March 2nd, 2025
#
################################################################################################


#TO DO: Make one mega csv combiner, then trunk data, and reimport into DB new data

import csv
import re
import pymysql
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import msvcrt
from sshtunnel import SSHTunnelForwarder

#database connection: enter in your own information
db_config = {
    "host": "159.203.140.48",
    "user": "fireworks", #database username
    "password": "fireworks", #database password
    "database": "fireworks"
}
ssh_host = '159.203.140.48'
ssh_port = 22
ssh_username = 'CSVparser'      
downloads_folder = os.path.join(os.path.expanduser("~"), "Desktop")
csv_file_path = os.path.join(downloads_folder, 'id_rsa_fireworks.key')
mysql_host = '127.0.0.1'  # MySQL server, localhost because we're tunneling
mysql_port = 3306
mysql_user = 'fireworks'
mysql_password = 'fireworks'
mysql_db = 'fireworks'

#extract ticket type and quantity from the ticket string
def extract_ticket_info(ticket_str):
    match = re.search(r"(.+?)\s*-(?!.*-)\s*(\d+)", ticket_str) #gets text before '-' as the type and after as the quantity
    if match:
        ticket_type = match.group(1).strip()
        quantity = int(match.group(2))
        return ticket_type, quantity
    return None, 0

#insert data into the Orders table
def insert_order(cursor, orderid, fullname, is_member, ticket_type, quantity, event_date):
    column_map = { 
        "Premium Parking": "premiumPermitQuantity",
        "FREE General Parking": "generalPermitQuantity",
        "Additional Parking": "additionalgeneralPermitQuantity",
        "Adult (15+)": "adultWristbandQuantity",
        "Youth (Infant - 14)": "youthWristbandQuantity"
    }

    if ticket_type in column_map:
        column_name = column_map[ticket_type]
        
        #sql query to insert the data or update an already existing order
        sql = f"""INSERT INTO Orders (orderid, fullname, isMember, {column_name}, dayOfAttend)  
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE {column_name} = {quantity};"""
        
        cursor.execute(sql, (orderid, fullname, is_member, quantity, event_date))

#read CSV and import data
def import_csv_to_db(csv_filename):
    try:
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_pkey=csv_file_path,         ##Big
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

            with open(csv_filename, newline="", encoding="utf-8") as csvfile:
                csv_reader = csv.reader(csvfile)

                event_date = None #variable to hold dayOfAttend's event date, cannot be inserted as null
                for row in csv_reader:
                    if len(row) >= 2 and "Fireworks" in row[0]:  #Look for event details row
                        try:
                            event_date = datetime.strptime(row[1].strip(), "%m/%d/%Y").date()
                        except ValueError:
                            print(f"Error: Invalid event date format in CSV: {row[1]}")
                            return False
                        break

                if not event_date:
                    print("Error: Event date not found in CSV.")
                    return False

                #skip headers and blank rows
                for _ in range(3):  
                    next(csv_reader, None)

                records_processed = 0
                for row in csv_reader: #process every row in csv, extract and clean variables     
                    if len(row) >= 5 and row[0].strip():
                        orderid = row[3].strip()
                        fullname = row[0].strip()
                        is_member = row[1].strip().lower() == "yes" 
                        ticket_type, quantity = extract_ticket_info(row[2])
                        if ticket_type: #ticket type validity check
                            print(orderid, fullname, is_member, ticket_type, quantity, event_date)
                            insert_order(cursor, orderid, fullname, is_member, ticket_type, quantity, event_date)                            
                            records_processed += 1
                        else:
                            print(fullname)

            connection.commit() #save changes to database
            cursor.close()
            connection.close()
            print(f"Success! {records_processed} records imported.")
            return True
    except pymysql.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# Function to select CSV file
def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Ticket Detail Report CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path


# Function to detect key press without pressing Enter (Windows only)
def wait_for_keypress():
    print("Press 'q' to quit or any other key to continue.")
    key = msvcrt.getch().decode("utf-8").lower()
    if key == 'q':
        return False
    else:
        return True

# Main function
def main():
    repeat = True
    while repeat:
        try:
            # Allow user to select CSV file
            csv_file = select_csv_file()
            if not csv_file:
                print("No file selected. Exiting.")
                return
                
            # Import the data
            success = import_csv_to_db(csv_file)
            
            # Show message based on result
            root = tk.Tk()
            root.withdraw()
            if success:
                messagebox.showinfo("Success", "The CSV data has been imported successfully!")
            else:
                messagebox.showerror("Error", "Failed to import data. Check the console for details.")
                
            repeat = wait_for_keypress()  # If 'q' is pressed, it exits the loop, otherwise continues
            
        except Exception as e:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            
################################################################################################

# Run script
if __name__ == "__main__":
    main()