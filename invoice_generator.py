import os
import tkinter as tk
from tkinter import messagebox, ttk
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

# Get next invoice number
def get_next_invoice_no():
    records = sheet.get_all_records()
    return f"INV-{len(records) + 1:03d}"

# Upload PDF to Google Drive
def upload_to_drive(file_path):
    drive_service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": os.path.basename(file_path), "mimeType": "application/pdf"}
    media = MediaFileUpload(file_path, mimetype="application/pdf")
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    drive_service.permissions().create(
        fileId=file['id'],
        body={"role": "reader", "type": "anyone"}
    ).execute()

    return f"https://drive.google.com/file/d/{file['id']}"

# Generate Invoice
def generate_invoice():
    invoice_no = get_next_invoice_no()
    customer_name = customer_name_entry.get().strip()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    items = []
    subtotal = 0
    for row in item_entries:
        desc, qty, price = row[0].get().strip(), int(row[1].get()), float(row[2].get())
        total_price = qty * price
        items.append([desc, qty, price, total_price])
        subtotal += total_price

    tax = subtotal * 0.18  # 18% GST
    grand_total = subtotal + tax
    payment_mode = payment_var.get()

    # Generate PDF Invoice
    pdf_filename = f"Invoice_{invoice_no}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # Invoice Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, "ABC Hardware Store")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Customer: {customer_name}")
    c.drawString(400, height - 80, f"Bill No.: {invoice_no}")
    c.drawString(400, height - 95, f"Date: {date_time}")
    c.line(50, height - 110, 550, height - 110)

    # Product Table
    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Product")
    c.drawString(200, y, "Quantity")
    c.drawString(300, y, "Unit Price (Rs)")
    c.drawString(450, y, "Total Price (Rs)")
    y -= 20

    c.setFont("Helvetica", 12)
    for desc, qty, price, total_price in items:
        c.drawString(50, y, desc)
        c.drawString(200, y, str(qty))
        c.drawString(300, y, f"Rs {price:.2f}")
        c.drawString(450, y, f"Rs {total_price:.2f}")
        y -= 25

    c.line(50, y, 550, y)
    y -= 20

    # Total Amount
    c.drawString(300, y, "Subtotal:")
    c.drawString(450, y, f"Rs {subtotal:.2f}")
    y -= 20
    c.drawString(300, y, "GST (18%):")
    c.drawString(450, y, f"Rs {tax:.2f}")
    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, y, "Grand Total:")
    c.drawString(450, y, f"Rs {grand_total:.2f}")
    c.line(50, y - 10, 550, y - 10)
    y -= 40

    # Payment Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Payment Mode:")
    c.drawString(200, y, payment_mode)

    c.save()

    # Upload PDF
    pdf_url = upload_to_drive(pdf_filename)

    # Save to Google Sheets
    sheet.append_row([invoice_no, customer_name, date_time, subtotal, tax, grand_total, payment_mode, pdf_url])

    messagebox.showinfo("Success", f"Invoice {invoice_no} saved!")

# Add Item Row
def add_item_row():
    row = []
    for i in range(3):
        entry = tk.Entry(frame, width=20)
        entry.grid(row=len(item_entries) + 1, column=i, padx=5, pady=5)
        entry.bind("<KeyPress>", on_key)
        row.append(entry)
    item_entries.append(row)

# Key Navigation
def on_key(event):
    if event.keysym in ("Return", "Right", "Down"):
        event.widget.tk_focusNext().focus()
    elif event.keysym in ("Left", "Up"):
        event.widget.tk_focusPrev().focus()

# UI Setup
root = tk.Tk()
root.title("Invoice Generator")
root.geometry("700x550")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Customer Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
customer_name_entry = tk.Entry(frame, width=30)
customer_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
customer_name_entry.bind("<KeyPress>", on_key)

item_entries = []
tk.Label(frame, text="Items").grid(row=1, column=0, padx=5, pady=10, sticky="w")
tk.Label(frame, text="Product").grid(row=2, column=0, padx=5, pady=5)
tk.Label(frame, text="Quantity").grid(row=2, column=1, padx=5, pady=5)
tk.Label(frame, text="Unit Price (Rs)").grid(row=2, column=2, padx=5, pady=5)

add_item_row()
tk.Button(frame, text="Add Item", command=add_item_row).grid(row=100, column=0, padx=5, pady=10)
payment_var = tk.StringVar(value="Cash")
payment_options = ttk.Combobox(frame, textvariable=payment_var, values=["Cash", "Credit Card", "UPI"])
payment_options.grid(row=101, column=1, padx=5, pady=5)
tk.Button(frame, text="Generate Invoice", command=generate_invoice, bg="blue", fg="white").grid(row=102, column=0, columnspan=2, padx=5, pady=20)
root.mainloop()

