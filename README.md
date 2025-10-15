# Client Query Management System (CQMS)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

A real-time web-based **Client Query Management System (CQMS)** that connects clients and support teams for efficient query submission, tracking, and management using **Streamlit**, **Python**, and **MySQL**.

---

## Table of Contents

1. Overview
2. Problem Statement
3. Business Use Cases
4. Approach
5. Features
6. Tech Stack
7. Installation Guide
    - Python Installation
    - Virtual Environment Setup
    - Install Streamlit and Dependencies
    - MySQL Installation & Configuration
    - Database Setup
    - Run the Streamlit App
8. Results
9. License
10. Author

---

## Overview

The **Client Query Management System (CQMS)** provides an interactive web interface for clients to submit queries and for support teams to efficiently manage them.  
It ensures faster resolution, better communication, and transparency in support processes.

---

## Problem Statement

The goal is to build a real-time **query management platform** using Streamlit and MySQL that:

- Allows clients to raise queries easily.  
- Lets support teams manage, close, and track query statuses.  
- Improves resolution time and customer satisfaction.  
- Uses **MySQL** as the backend and **Streamlit** for frontend visualization.

---

## Business Use Cases

✅ **Query Submission Interface** – Clients can raise queries with details.  
✅ **Query Tracking Dashboard** – Support team can view and close queries.  
✅ **Service Efficiency** – Monitor how quickly queries are resolved.  
✅ **Customer Satisfaction** – Faster response = happier clients.  
✅ **Support Load Monitoring** – Identify recurring or backlog issues.

---

##  Approach

### 1. Login System (Client & Support)

- Secure login for both Client and Support users.
- Passwords hashed using `hashlib.sha256(password.encode()).hexdigest()`.
- User credentials stored in MySQL with fields:  
  - `username (TEXT)`  
  - `hashed_password (TEXT)`  
  - `role (TEXT)`

### Login Flow

1. User enters **Username**, **Password**, and **Role (Client/Support)**.  
2. System hashes the password and validates against the database.  
3. Upon success:
   - Client → Redirected to **Client Query Page**  
   - Support → Redirected to **Support Dashboard**

---

### 2. Query Insertion Page (Client Side)

**Inputs:**
- Email ID  
- Mobile Number  
- Query Heading  
- Query Description  

**On Submission:**
- `query_created_time` auto-generated using `datetime.now()`  
- `status` set as `"Open"` by default  
- `query_closed_time` remains `NULL`

---

### 3. Query Management Page (Support Team Side)

Support team can:
- View and filter queries by **Open/Closed** status  
- Select and close a query  
- Update status and auto-set closure time using `datetime.now()`

---

## Features

- Real-time Query Submission  
- Role-based Login (Client / Support)  
- Query Filtering and Closure  
- MySQL Integration  
- Auto Timestamping  
- Streamlit-based UI  
- Optional Image Upload Support  

---

## Tech Stack

| Category | Technology |
|-----------|-------------|
| **Language** | Python 3.13+ |
| **Frontend** | Streamlit |
| **Backend** | Python |
| **Database** | MySQL |
| **Libraries** | Pandas, Datetime, Hashlib, MySQL Connector |
| **OS Support** | Windows, Ubuntu |

---

## Installation Guide

### Python Installation

🔹 **Windows:**
1. Go to [Python Downloads](https://www.python.org/downloads/)
2. Download and install the latest version (check **“Add Python to PATH”** during installation)
3. Verify installation:
   ```bash
   python --version

### Create Virtual Environment

    python -m venv cqmsvenv
    cqmsvenv\Scripts\Activate.ps1

### Install Streamlit and Dependencies

    Install the required libraries:

    pip install streamlit pandas mysql-connector-python

### Install MySQL and Configure

🔹 **Windows:**
1. Download and install MySQL Community Server

2. During setup, set:
    
    Username: root
    Password: <your_password>

3. Verify installation:
    
    mysql -u root -p

### Database Setup
    Once inside MySQL terminal:

-- Create a database

    CREATE DATABASE cqms_db;

-- Use the database

    USE cqms_db;

-- Create table for users
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  hashed_password VARCHAR(256),
  role VARCHAR(20)
);

-- Create table for queries
CREATE TABLE query_management (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mail_id VARCHAR(100),
  mobile_number VARCHAR(15),
  query_heading VARCHAR(255),
  query_description VARCHAR(255),
  query_status VARCHAR(20),
  query_created_time DATETIME,
  query_closed_time DATETIME NULL
);



### Run the app
    Create a file named cqms_app.py and include your Streamlit app code.
    Then run the application using:

    streamlit run cqms_app.py

    After running, you’ll see something like:

      You can now view your Streamlit app in your browser.

      Local URL: http://localhost:8501
