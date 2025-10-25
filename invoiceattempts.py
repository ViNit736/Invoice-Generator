# import os
# import tkinter as tk
# from tkinter import messagebox
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from datetime import datetime
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# # Google Sheets & Drive Setup
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
# client = gspread.authorize(creds)
# sheet = client.open("Invoices").sheet1

# def get_next_invoice_no():
#     records = sheet.get_all_records()
#     return f"INV-{len(records) + 1:03d}"  # Generates invoice number like INV-001, INV-002

# def upload_to_drive(file_path):
#     drive_service = build("drive", "v3", credentials=creds)
#     file_metadata = {"name": os.path.basename(file_path), "mimeType": "application/pdf"}
#     media = MediaFileUpload(file_path, mimetype="application/pdf")
#     file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
#     return f"https://drive.google.com/file/d/{file['id']}"

# def generate_invoice():
#     invoice_no = get_next_invoice_no()
#     customer_name = customer_name_entry.get()
#     date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     items = []
#     sheet_items = []
#     for row in item_entries:
#         desc, qty, price = row[0].get(), int(row[1].get()), float(row[2].get())
#         total_price = qty * price
#         items.append((desc, qty, price, total_price))
#         sheet_items.append([invoice_no, customer_name, date_time, desc, qty, price, total_price])
    
#     subtotal = sum(qty * price for _, qty, price, _ in items)
#     tax = subtotal * 0.05
#     total = subtotal + tax
#     payment_mode = payment_var.get()
    
#     pdf_filename = f"Invoice_{invoice_no}.pdf"
#     c = canvas.Canvas(pdf_filename, pagesize=A4)
#     width, height = A4
    
#     # Header
#     c.setFont("Helvetica-Bold", 16)
#     c.drawString(200, height - 50, "ABC Hardware Store")
#     c.setFont("Helvetica", 10)
#     c.drawString(50, height - 80, f"Customer: {customer_name}")
#     c.drawString(400, height - 80, f"Bill No.: {invoice_no}")
#     c.drawString(400, height - 95, f"Date: {date_time}")
#     c.line(50, height - 110, 550, height - 110)
    
#     # Product Table
#     y = height - 130
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(50, y, "Product")
#     c.drawString(250, y, "Quantity")
#     c.drawString(350, y, "Unit Price")
#     c.drawString(450, y, "Total Price")
#     y -= 20
    
#     c.setFont("Helvetica", 10)
#     for desc, qty, price, total_price in items:
#         c.drawString(50, y, desc)
#         c.drawString(250, y, str(qty))
#         c.drawString(350, y, f"${price:.2f}")
#         c.drawString(450, y, f"${total_price:.2f}")
#         y -= 20
    
#     c.line(50, y, 550, y)
    
#     # Total Amount
#     c.drawString(350, y - 20, "Subtotal:")
#     c.drawString(450, y - 20, f"${subtotal:.2f}")
#     c.drawString(350, y - 40, "Tax (5%):")
#     c.drawString(450, y - 40, f"${tax:.2f}")
#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(350, y - 60, "Grand Total:")
#     c.drawString(450, y - 60, f"${total:.2f}")
#     c.line(50, y - 80, 550, y - 80)
    
#     # Payment Details
#     c.setFont("Helvetica-Bold", 10)
#     c.drawString(50, y - 100, "Payment Mode:")
#     c.drawString(200, y - 100, payment_mode)
    
#     # Footer
#     c.setFont("Helvetica", 9)
#     c.drawString(180, y - 140, "Thank you for your business! Contact: (555) 123-4567 | abcstore@example.com")
#     c.line(50, y - 150, 550, y - 150)
    
#     c.save()
    
#     # Upload PDF to Google Drive
#     pdf_url = upload_to_drive(pdf_filename)
    
#     # Save to Google Sheets (Tabular Format)
#     sheet.append_row([invoice_no, customer_name, date_time, "", "", "", "", subtotal, tax, total, payment_mode, pdf_url])
#     for row in sheet_items:
#         row.append(pdf_url)
#         sheet.append_row(row)
    
#     messagebox.showinfo("Success", f"Invoice {invoice_no} saved as {pdf_filename} and recorded in Google Sheets with PDF link")

# def add_item_row():
#     row = []
#     for i in range(3):
#         entry = tk.Entry(tk_window, width=15)
#         entry.grid(row=len(item_entries) + 4, column=i)
#         row.append(entry)
#     item_entries.append(row)

# def on_enter(event):
#     event.widget.tk_focusNext().focus()

# tk_window = tk.Tk()
# tk_window.title("Invoice Generator")
# tk_window.geometry("500x400")

# tk.Label(tk_window, text="Customer Name").grid(row=0, column=0)
# customer_name_entry = tk.Entry(tk_window)
# customer_name_entry.grid(row=0, column=1)
# customer_name_entry.bind("<Return>", on_enter)

# tk.Label(tk_window, text="Items").grid(row=2, column=0)
# tk.Label(tk_window, text="Product").grid(row=3, column=0)
# tk.Label(tk_window, text="Quantity").grid(row=3, column=1)
# tk.Label(tk_window, text="Unit Price").grid(row=3, column=2)

# item_entries = []
# add_item_row()

# tk.Button(tk_window, text="Add Item", command=add_item_row).grid(row=100, column=0)

# tk.Label(tk_window, text="Payment Mode").grid(row=101, column=0)
# payment_var = tk.StringVar(value="Cash")
# tk.OptionMenu(tk_window, payment_var, "Cash", "Credit Card", "UPI").grid(row=101, column=1)

# tk.Button(tk_window, text="Generate Invoice", command=generate_invoice).grid(row=102, column=0, columnspan=2)

# tk_window.mainloop()
import os
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Sheets & Drive Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Invoices").sheet1

def get_next_invoice_no():
    """Generates the next invoice number automatically."""
    records = sheet.get_all_records()
    return f"INV-{len(records) + 1:03d}"  # Generates invoice like INV-001, INV-002

def upload_to_drive(file_path):
    """Uploads PDF invoice to Google Drive and returns a shareable link."""
    drive_service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": os.path.basename(file_path), "mimeType": "application/pdf"}
    media = MediaFileUpload(file_path, mimetype="application/pdf")
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    # Make file publicly accessible
    drive_service.permissions().create(
        fileId=file["id"],
        body={"role": "reader", "type": "anyone"}
    ).execute()

    return f"https://drive.google.com/file/d/{file['id']}/view"

def generate_invoice():
    """Generates invoice, saves to PDF, uploads to Drive, and records in Google Sheets."""
    invoice_no = get_next_invoice_no()
    customer_name = customer_name_entry.get()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    items = []
    sheet_data = [[invoice_no, customer_name, date_time, "Product", "Quantity", "Unit Price", "Total Price"]]

    for row in item_entries:
        desc, qty, price = row[0].get(), row[1].get(), row[2].get()
        if not desc or not qty or not price:
            continue
        qty, price = int(qty), float(price)
        total_price = qty * price
        items.append((desc, qty, price, total_price))
        sheet_data.append([invoice_no, customer_name, date_time, desc, qty, price, total_price])
    
    subtotal = sum(item[3] for item in items)
    tax = subtotal * 0.05
    total = subtotal + tax
    payment_mode = payment_var.get()

    # Generate PDF
    pdf_filename = f"Invoice_{invoice_no}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "ABC Hardware Store")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Customer: {customer_name}")
    c.drawString(400, height - 80, f"Bill No.: {invoice_no}")
    c.drawString(400, height - 95, f"Date: {date_time}")
    c.line(50, height - 110, 550, height - 110)

    # Product Table
    y = height - 130
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Product")
    c.drawString(250, y, "Quantity")
    c.drawString(350, y, "Unit Price")
    c.drawString(450, y, "Total Price")
    y -= 20

    c.setFont("Helvetica", 10)
    for desc, qty, price, total_price in items:
        c.drawString(50, y, desc)
        c.drawString(250, y, str(qty))
        c.drawString(350, y, f"${price:.2f}")
        c.drawString(450, y, f"${total_price:.2f}")
        y -= 20

    c.line(50, y, 550, y)

    # Total Amount
    c.drawString(350, y - 20, "Subtotal:")
    c.drawString(450, y - 20, f"${subtotal:.2f}")
    c.drawString(350, y - 40, "Tax (5%):")
    c.drawString(450, y - 40, f"${tax:.2f}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y - 60, "Grand Total:")
    c.drawString(450, y - 60, f"${total:.2f}")
    c.line(50, y - 80, 550, y - 80)

    # Payment Details
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y - 100, "Payment Mode:")
    c.drawString(200, y - 100, payment_mode)

    # Footer
    c.setFont("Helvetica", 9)
    c.drawString(180, y - 140, "Thank you for your business! Contact: (555) 123-4567 | abcstore@example.com")
    c.line(50, y - 150, 550, y - 150)

    c.save()

    # Upload PDF and save to Google Sheets
    pdf_url = upload_to_drive(pdf_filename)
    sheet.append_row([invoice_no, customer_name, date_time, subtotal, tax, total, payment_mode, pdf_url])
    for row in sheet_data:
        row.append(pdf_url)
        sheet.append_row(row)

    messagebox.showinfo("Success", f"Invoice {invoice_no} saved and uploaded!")

def add_item_row():
    """Adds a new row for item input."""
    row = []
    for i in range(3):
        entry = tk.Entry(tk_window, width=15)
        entry.grid(row=len(item_entries) + 4, column=i)
        row.append(entry)
    item_entries.append(row)

# Tkinter UI
tk_window = tk.Tk()
tk_window.title("Invoice Generator")
tk_window.geometry("500x400")

tk.Label(tk_window, text="Customer Name").grid(row=0, column=0)
customer_name_entry = tk.Entry(tk_window)
customer_name_entry.grid(row=0, column=1)

tk.Label(tk_window, text="Items").grid(row=2, column=0)
tk.Label(tk_window, text="Product").grid(row=3, column=0)
tk.Label(tk_window, text="Quantity").grid(row=3, column=1)
tk.Label(tk_window, text="Unit Price").grid(row=3, column=2)

item_entries = []
add_item_row()

tk.Button(tk_window, text="Add Item", command=add_item_row).grid(row=100, column=0)

tk.Label(tk_window, text="Payment Mode").grid(row=101, column=0)
payment_var = tk.StringVar(value="Cash")
tk.OptionMenu(tk_window, payment_var, "Cash", "Credit Card", "UPI").grid(row=101, column=1)

tk.Button(tk_window, text="Generate Invoice", command=generate_invoice).grid(row=102, column=0, columnspan=2)

tk_window.mainloop()
