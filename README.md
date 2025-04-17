# Hagley Fireworks Ticket Management System

**IT493 Capstone Project**  
A Ticket Management System for the Hagley Museum, providing solutions for ticket validation, ticket inventory management, and record reconciliation.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Structure](#database-structure)
- [File Descriptions](#file-descriptions)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
The Hagley Fireworks Ticket Management System is a comprehensive solution designed to manage the Hagley Museum's annual fireworks event. It includes functionality for:
- Ticket inventory management.
- Ticket validation.
- Record reconciliation.

This project includes a web-based interface, database setup, and additional tools and utilities to streamline event management.

---

## Features
- **Ticket Validation:** Verify ticket authenticity and prevent duplication.
- **Ticket Inventory Management:** Track and manage ticket sales and availability.
- **Record Reconciliation:** Generate reports and reconcile event records for auditing.
- **Statistical Dashboards:** View statistics for different dates of the event (via stored procedures).
- **Database Integrity:** Ensure database consistency with constraints and validations.

---

## Installation

### Prerequisites
- MySQL Server
- A web server (e.g., Apache or Nginx)
- PHP (if applicable for the web interface)
- Git (for cloning the repository)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Charlesnorris509/Hagley-Fireworks.git
   cd Hagley-Fireworks

## 1. Set Up the MySQL Database

Run the provided SQL script to create the database and set up the required tables:

### Log in to your MySQL server:
```bash
mysql -u <username> -p
```

### Create the database and import the SQL script:
```sql
SOURCE DB_Fireworks_V2.4.sql;
```

This script will:
- Create the fireworks database if it doesn't already exist.
- Establish the Orders and Users tables.
- Add stored procedures such as DashboardOutDay1 and DashboardOutDay2 for generating event statistics.

## 2. Deploy the Application

Place the repository files in the root directory of your web server.
For example, if using Apache, move the files to /var/www/html/Hagley-Fireworks:

```bash
sudo cp -r . /var/www/html/Hagley-Fireworks
```

## 3. Configure Permissions

Ensure the web server has proper permissions to access the application files:

```bash
sudo chown -R www-data:www-data /var/www/html/Hagley-Fireworks
sudo chmod -R 755 /var/www/html/Hagley-Fireworks
```

## 4. Configure the Web Server

Set up a virtual host for the application. For example, in Apache:

```apache
<VirtualHost *:80>
    ServerName hagleyfireworks.local
    DocumentRoot /var/www/html/Hagley-Fireworks

    <Directory /var/www/html/Hagley-Fireworks>
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/hagleyfireworks_error.log
    CustomLog ${APACHE_LOG_DIR}/hagleyfireworks_access.log combined
</VirtualHost>
```

Enable the new configuration and restart Apache:

```bash
sudo a2ensite hagleyfireworks.conf
sudo systemctl restart apache2
```

