from tkinter import *
from tkinter import ttk, messagebox
import datetime as dt
from mydb import *

# Database object
data = Database(db='invoice.db')

# Global variables
selected_rowid = 0
count = 0

# Functions
def setDate():
    date = dt.datetime.now()
    invoice_date_var.set(f'{date:%d %B %Y}')

def clearEntries():
    invoice_number.delete(0, END)
    invoice_value.delete(0, END)
    invoice_date.delete(0, END)
    client_number.delete(0, END)
    client_name.delete(0, END)
    gl_account.delete(0, END)

def saveRecord():
    data.insertRecord(
        invoice_number_var.get(),
        invoice_value_var.get(),
        invoice_date_var.get(),
        client_number_var.get(),
        client_name_var.get(),
        gl_account_var.get()
    )
    refreshData()

def fetch_records():
    global count
    records = data.fetchRecord('SELECT rowid, * FROM invoice_record')
    for rec in records:
        tv.insert('', 'end', iid=count, values=rec)
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        invoice_number_var.set(val[1])
        invoice_value_var.set(val[2])
        invoice_date_var.set(val[3])
        client_number_var.set(val[4])
        client_name_var.set(val[5])
        gl_account_var.set(val[6])
    except Exception as ep:
        print("Selection error:", ep)

def update_record():
    global selected_rowid
    selected = tv.focus()
    try:
        data.updateRecord(
            invoice_number_var.get(),
            invoice_value_var.get(),
            invoice_date_var.get(),
            client_number_var.get(),
            client_name_var.get(),
            gl_account_var.get(),
            selected_rowid
        )
        tv.item(selected, text="", values=(
            selected_rowid,
            invoice_number_var.get(),
            invoice_value_var.get(),
            invoice_date_var.get(),
            client_number_var.get(),
            client_name_var.get(),
            gl_account_var.get()
        ))
    except Exception as ep:
        messagebox.showerror('Error', ep)
    clearEntries()
    tv.after(400, refreshData)

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

# GUI setup
ws = Tk()
ws.title('Invoice Tracker')

f = ('Times New Roman', 14)

# Variables
invoice_number_var = StringVar()
invoice_value_var = DoubleVar()
invoice_date_var = StringVar()
client_number_var = StringVar()
client_name_var = StringVar()
gl_account_var = StringVar()

# Frames
f2 = Frame(ws)
f2.pack()

f1 = Frame(ws, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

# Labels
Label(f1, text='Invoice Number', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='Invoice Value', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='Invoice Date', font=f).grid(row=2, column=0, sticky=W)
Label(f1, text='Client Number', font=f).grid(row=3, column=0, sticky=W)
Label(f1, text='Client Name', font=f).grid(row=4, column=0, sticky=W)
Label(f1, text='GL Account', font=f).grid(row=5, column=0, sticky=W)

# Entry widgets
invoice_number = Entry(f1, font=f, textvariable=invoice_number_var)
invoice_value = Entry(f1, font=f, textvariable=invoice_value_var)
invoice_date = Entry(f1, font=f, textvariable=invoice_date_var)
client_number = Entry(f1, font=f, textvariable=client_number_var)
client_name = Entry(f1, font=f, textvariable=client_name_var)
gl_account = Entry(f1, font=f, textvariable=gl_account_var)

# Grid placement
invoice_number.grid(row=0, column=1, padx=10, sticky=EW)
invoice_value.grid(row=1, column=1, padx=10, sticky=EW)
invoice_date.grid(row=2, column=1, padx=10, sticky=EW)
client_number.grid(row=3, column=1, padx=10, sticky=EW)
client_name.grid(row=4, column=1, padx=10, sticky=EW)
gl_account.grid(row=5, column=1, padx=10, sticky=EW)

# Buttons
Button(f1, text='Set Date', font=f, bg='#04C4D9', command=setDate).grid(row=2, column=2, padx=10, sticky=EW)
Button(f1, text='Save', font=f, bg='#42602D', fg='white', command=saveRecord).grid(row=0, column=2, padx=10, sticky=EW)
Button(f1, text='Clear', font=f, bg='#D9B036', fg='white', command=clearEntries).grid(row=1, column=2, padx=10, sticky=EW)
Button(f1, text='Update', font=f, bg='#C2BB00', command=update_record).grid(row=3, column=2, padx=10, sticky=EW)
Button(f1, text='Delete', font=f, bg='#BD2A2E', command=deleteRow).grid(row=4, column=2, padx=10, sticky=EW)
Button(f1, text='Exit', font=f, bg='#D33532', fg='white', command=ws.destroy).grid(row=5, column=2, padx=10, sticky=EW)

# Treeview
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=8)
tv.pack(side="left")

tv.heading(1, text="Row ID")
tv.heading(2, text="Invoice Number")
tv.heading(3, text="Invoice Value")
tv.heading(4, text="Invoice Date")
tv.heading(5, text="Client Number")
tv.heading(6, text="Client Name")
tv.heading(7, text="GL Account")

for i in range(1, 8):
    tv.column(i, anchor=CENTER)

tv.bind("<ButtonRelease-1>", select_record)

# Scrollbar
scrollbar = Scrollbar(f2, orient='vertical', command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# Load data
fetch_records()



search_var = StringVar()

search_entry = Entry(f1, font=f, textvariable=search_var)
search_entry.grid(row=6, column=0, columnspan=2, sticky=EW, padx=10)

Button(f1, text='Search', font=f, bg='#6A5ACD', fg='white', command=lambda: searchRecords(search_var.get())).grid(row=6, column=2, padx=10, sticky=EW)

def searchRecords(keyword):
    for item in tv.get_children():
        tv.delete(item)
    query = f"""
        SELECT rowid, * FROM invoice_record
        WHERE invoice_number LIKE '%{keyword}%'
        OR client_name LIKE '%{keyword}%'
    """
    results = data.fetchRecord(query)
    for i, rec in enumerate(results):
        tv.insert('', 'end', iid=i, values=rec)


import csv

def exportToCSV():
    records = data.fetchRecord("SELECT rowid, * FROM invoice_record")
    with open("invoices.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Row ID", "Invoice Number", "Invoice Value", "Invoice Date", "Client Number", "Client Name", "GL Account"])
        writer.writerows(records)
    messagebox.showinfo("Export", "Data exported to invoices.csv")

Button(f1, text='Export CSV', font=f, bg='#228B22', fg='white', command=exportToCSV).grid(row=7, column=0, columnspan=3, sticky=EW, padx=10)


def summarizeGL():
    query = """
        SELECT gl_account, SUM(invoice_value)
        FROM invoice_record
        GROUP BY gl_account
    """
    results = data.fetchRecord(query)
    summary = "\n".join([f"{gl}: {total:.2f}" for gl, total in results])
    messagebox.showinfo("GL Summary", f"Invoice Totals by GL Account:\n\n{summary}")

Button(f1, text='GL Summary', font=f, bg='#8B0000', fg='white', command=summarizeGL).grid(row=7, column=3, sticky=EW, padx=10)


start_date_var = StringVar()
end_date_var = StringVar()

Label(f1, text='Start Date (DD-MM-YYYY)', font=f).grid(row=8, column=0, sticky=W)
start_date_entry = Entry(f1, font=f, textvariable=start_date_var)
start_date_entry.grid(row=8, column=1, padx=10, sticky=EW)

Label(f1, text='End Date (DD-MM-YYYY)', font=f).grid(row=9, column=0, sticky=W)
end_date_entry = Entry(f1, font=f, textvariable=end_date_var)
end_date_entry.grid(row=9, column=1, padx=10, sticky=EW)




def filterByDate():
    start = start_date_var.get()
    end = end_date_var.get()

    try:
        # Convert to proper format if needed
        start_dt = dt.datetime.strptime(start, "%d-%m-%Y").date()
        end_dt = dt.datetime.strptime(end, "%d-%m-%Y").date()

        query = f"""
            SELECT rowid, * FROM invoice_record
            WHERE invoice_date BETWEEN '{start_dt}' AND '{end_dt}'
        """
        results = data.fetchRecord(query)

        for item in tv.get_children():
            tv.delete(item)

        for i, rec in enumerate(results):
            tv.insert('', 'end', iid=i, values=rec)

    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter dates in DD-MM-YYYY format.")

Button(f1, text='Filter by Date Range', font=f, bg='#4682B4', fg='white', command=filterByDate).grid(row=9,
            column=2, padx=10, sticky=EW)



# Run app
ws.mainloop()

