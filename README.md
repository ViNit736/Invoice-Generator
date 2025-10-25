# 🧾 Smart Invoice Generator

## 📘 Overview
Smart Invoice Generator is a Python-based desktop app that automates invoice creation. Built with **Tkinter**, it lets users add customer and product details, auto-calculates totals with **GST**, and generates professional **PDF invoices**. Each invoice is uploaded to **Google Drive**, and details are logged in **Google Sheets** for easy tracking.

## ⚙️ Features
- Auto-calculates subtotal, GST (18%), and total  
- Generates PDF invoices using **ReportLab**  
- Uploads PDFs to **Google Drive**  
- Logs data in **Google Sheets**  
- Auto-incremented invoice numbers  
- Supports Cash, UPI, and Card payments  
- Simple, user-friendly GUI  

## 🛠️ Tech Stack
- **Language:** Python  
- **Libraries:** tkinter, reportlab, gspread, googleapiclient, oauth2client  

## 🚀 Setup & Usage
1. Clone the repo  
   ```bash
   git clone https://github.com/yourusername/smart-invoice-generator.git
   cd smart-invoice-generator
````

2. Install dependencies

   ```bash
   pip install gspread oauth2client google-api-python-client reportlab
   ```
3. Add your Google service account credentials file as `google_credentials.json`.
4. Ensure Google Sheets (“Invoices”) and Drive API are enabled.
5. Run the app

   ```bash
   python invoice_generator.py
   ```

## 📂 Output

* PDF invoices saved locally and on Google Drive
* Invoice data automatically added to Google Sheets

## 📈 Future Enhancements

* Email invoices directly to customers
* Add search/filter options
* Generate monthly reports

## 👨‍💻 Author

Developed by **[Your Name]**
A simple, automated, and paperless billing solution.
