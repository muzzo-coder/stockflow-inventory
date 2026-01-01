# StockFlow — Inventory Management System

## 📌 Overview
StockFlow is a complete inventory management solution designed to help businesses manage products, warehouses, suppliers, and sales in real time.  
This project demonstrates practical skills in **Flask, SQLAlchemy, REST APIs, and database design**.

---

## 🚀 Features
- ✔️ Company & warehouse management  
- ✔️ Product and stock tracking  
- ✔️ Supplier management and product linking  
- ✔️ Sales tracking with automatic inventory deduction  
- ✔️ SQLite database with structured schema  
- ✔️ Modular backend architecture

---

## 🏗️ Tech Stack
- **Backend:** Python, Flask, SQLAlchemy  
- **Database:** SQLite  
- **Tools:** Git, Virtual Environment

---

## 📂 Project Structure
backend/
app.py
models.py
routes/
env/
db/
schema.sql
README.md

---

## ▶️ How to Run Locally

### 1️⃣ Create virtual environment

python -m venv env

2️⃣ Activate it

Windows

env\Scripts\activate


Mac / Linux

source env/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Initialize database (if needed)

Make sure you are inside the project root:

sqlite3 db/database.db < db/schema.sql

5️⃣ Start the backend server
python backend/app.py


Server runs at:

http://127.0.0.1:5000

📄 Database Schema

All database tables and relations are defined in:

db/schema.sql
🎯 Project Purpose

This project is part of my learning and interview portfolio. It highlights:

Clean, maintainable backend structure

API development with Flask

Database design and relationships

Real-world inventory use-case implementation

🧪 Future Enhancements

Authentication & role-based access

Reporting and analytics dashboard

Frontend UI integration

Cloud deployment (Render / Railway / VPS)

👤 Author

Your Name : Mujjamil Sofi
Email : mujammilsofi2@gmail.com 
