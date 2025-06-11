from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, simpledialog, Toplevel, Frame, Label, ttk
import sqlite3


#database is created and connected
# cursor is an object used to run sql commands and interact with database
conn = sqlite3.connect('clinical.db')
c = conn.cursor()


# Creating patient and appointments table
c.execute('''CREATE TABLE IF NOT EXISTS patients (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             age INTEGER NOT NULL,
             gender TEXT NOT NULL,
             contact TEXT NOT NULL,
             disease TEXT NOT NULL,
             bill REAL NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS appointments (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             patient_name TEXT NOT NULL,
             date TEXT NOT NULL,
             time TEXT NOT NULL,
             reason TEXT NOT NULL)''')

#saves changes to database
conn.commit()


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/vipinchoudhary/Desktop/MediVerse/Dashboard_page/build/assets/frame0")


# defining colours
BG_COLOR = "#344865"
ENTRY_BG = "#4a6572"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#5b8cff"
FONT_NAME = "Arial"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_patient():
    form_window = Toplevel(window)
    form_window.title("Add New Patient")
    form_window.geometry("1100x733")
    form_window.configure(bg=BG_COLOR)
    
    main_frame = Frame(form_window, bg=BG_COLOR)
    main_frame.pack(pady=50, fill='both', expand=True)

    # Form Title
    Label(main_frame, text="NEW PATIENT REGISTRATION", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=(FONT_NAME, 50, "bold")).grid(row=0, column=0, columnspan=2, pady=30)

    # Input Fields
    fields = [
        ("Patient Name:", 1),
        ("Age:", 2),
        ("Gender (M/F/O):", 3),
        ("Contact Number:", 4),
        ("Disease:", 5),
        ("Bill Amount:", 6)
    ]

    # an empty list to store all the patients
    entries = []
    for text, row in fields:
        Label(main_frame, text=text, bg=BG_COLOR, fg=TEXT_COLOR, 
              font=(FONT_NAME, 26)).grid(row=row, column=0, padx=40, pady=15)
        entry = Entry(main_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=(FONT_NAME, 26), width=30)
        entry.grid(row=row, column=1, padx=40, pady=15)
        entries.append(entry)
        
        
    # nested function to check user input
    def validate_inputs():
        
        #values[0]: Name
        #values[1]: Age
        #values[2]: Gender
        #values[3]: Contact Number
        #values[4]: Disease
        #values[5]: Bill Amount
        values = [e.get() for e in entries]
        
        # ensures no field remains empty
        if not all(values):
            messagebox.showwarning("Empty Fields", "All fields must be filled!")
            return False
        
        #ensures age & bill are integer & float
        try:
            int(values[1])  # Age
            float(values[5])  # Bill Amount
        except ValueError:
            messagebox.showwarning("Invalid Input", "Age must be integer and Bill must be numeric")
            return False
        
        # for gender
        if values[2].upper() not in ['M', 'F', 'O']:
            messagebox.showwarning("Invalid Gender", "Gender must be M, F, or O")
            return False
        return True


    #nested function for saving data to database
    def save_patient():
        if not validate_inputs():
            return
        try:
            c.execute('''INSERT INTO patients 
                      (name, age, gender, contact, disease, bill)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                      (entries[0].get(),
                       int(entries[1].get()),
                       entries[2].get().upper(),
                       entries[3].get(),
                       entries[4].get(),
                       float(entries[5].get())))
            conn.commit()
            messagebox.showinfo("Success", "Patient record added successfully!")
            form_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    Button(main_frame, text="Save Patient Record", command=save_patient,
           bg=BUTTON_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 18, "bold"),
           width=30, height=2).grid(row=7, column=0, columnspan=2, pady=40)



def view_patients():
    view_window = Toplevel(window)
    view_window.title("Patient Records")
    view_window.geometry("1100x733")
    view_window.configure(bg=BG_COLOR)
    
    # creating main frame
    main_frame = Frame(view_window, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=50, pady=50)

    # for title
    Label(main_frame, text="PATIENT RECORDS", bg=BG_COLOR, fg=TEXT_COLOR,
          font=(FONT_NAME, 50, "bold")).pack(pady=20)

    # Treeview with styling
    style = ttk.Style()
    style.theme_use("default")
    
    # treeview is a part of ttk
    #treeview is used for displaying data in tabular form
    
    style.configure("Treeview", background=ENTRY_BG, fieldbackground=ENTRY_BG, 
                    foreground=TEXT_COLOR, font=(FONT_NAME, 16), rowheight=40)
    style.configure("Treeview.Heading", background=BUTTON_COLOR, 
                    foreground=TEXT_COLOR, font=(FONT_NAME, 18, "bold"))
    style.map("Treeview", background=[('selected', '#344865')])

    tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Age", "Gender", "Contact", "Disease", "Bill"),
                        show="headings", selectmode="browse")
    
    # Configure columns
    tree.column("ID", width=80, anchor='center')
    tree.column("Name", width=200, anchor='w')
    tree.column("Age", width=100, anchor='center')
    tree.column("Gender", width=120, anchor='center')
    tree.column("Contact", width=200, anchor='center')
    tree.column("Disease", width=250, anchor='w')
    tree.column("Bill", width=150, anchor='center')

    # Headings
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Contact", text="Contact")
    tree.heading("Disease", text="Disease")
    tree.heading("Bill", text="Bill")

    # Scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Layout
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load data
    try:
        #retrives all data from patient table
        c.execute("SELECT * FROM patients")
        
        #retrives all rows as list
        patients = c.fetchall()
        
        if not patients:
            messagebox.showinfo("No Records", "No patient records found")
            view_window.destroy()
            return
        
        for patient in patients:
            tree.insert("", "end", values=patient)
    
    # catches error when database is not connected or something        
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        view_window.destroy()


def add_appointment():
    
    form_window = Toplevel(window)
    form_window.title("Add New Appointment")
    form_window.geometry("1100x733")
    form_window.configure(bg=BG_COLOR)
    
    #adding a main frame
    main_frame = Frame(form_window, bg=BG_COLOR)
    main_frame.pack(pady=50, fill='both', expand=True)

    # for title
    Label(main_frame, text="NEW APPOINTMENT", bg=BG_COLOR, fg=TEXT_COLOR, 
          font=(FONT_NAME, 50, "bold")).grid(row=0, column=0, columnspan=2, pady=30)

    # Input Fields
    fields = [
        ("Patient Name:", 1),
        ("Date (YYYY-MM-DD):", 2),
        ("Time (HH:MM):", 3),
        ("Reason:", 4)
    ]

    entries = []
    for text, row in fields:
        Label(main_frame, text=text, bg=BG_COLOR, fg=TEXT_COLOR, 
              font=(FONT_NAME, 26)).grid(row=row, column=0, padx=40, pady=15)
        entry = Entry(main_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=(FONT_NAME, 26), width=30)
        entry.grid(row=row, column=1, padx=40, pady=15)
        entries.append(entry)

    def validate_inputs():
        values = [e.get() for e in entries]
        if not all(values):
            messagebox.showwarning("Empty Fields", "All fields must be filled!")
            return False
        return True

    def save_appointment():
        if not validate_inputs():
            return
        try:
            c.execute('''INSERT INTO appointments 
                      (patient_name, date, time, reason)
                      VALUES (?, ?, ?, ?)''',
                      (entries[0].get(),
                       entries[1].get(),
                       entries[2].get(),
                       entries[3].get()))
            conn.commit()
            messagebox.showinfo("Success", "Appointment added successfully!")
            form_window.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    Button(main_frame, text="Save Appointment", command=save_appointment,
           bg=BUTTON_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 18, "bold"),
           width=30, height=2).grid(row=5, column=0, columnspan=2, pady=40)



def view_appointments():
    
    view_window = Toplevel(window)
    view_window.title("Appointment Schedule")
    view_window.geometry("1100x733")
    view_window.configure(bg=BG_COLOR)
    
    main_frame = Frame(view_window, bg=BG_COLOR)
    main_frame.pack(fill="both", expand=True, padx=50, pady=50)

    # Title
    Label(main_frame, text="APPOINTMENT SCHEDULE", bg=BG_COLOR, fg=TEXT_COLOR,
          font=(FONT_NAME, 50, "bold")).pack(pady=20)

    # Treeview styling
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background=ENTRY_BG, fieldbackground=ENTRY_BG, 
                    foreground=TEXT_COLOR, font=(FONT_NAME, 16), rowheight=40)
    style.configure("Treeview.Heading", background=BUTTON_COLOR, 
                    foreground=TEXT_COLOR, font=(FONT_NAME, 18, "bold"))
    style.map("Treeview", background=[('selected', '#344865')])

    tree = ttk.Treeview(main_frame, columns=("ID", "Patient", "Date", "Time", "Reason"),
                        show="headings", selectmode="browse")
    
    
    tree.column("ID", width=80, anchor='center')
    tree.column("Patient", width=250, anchor='w')
    tree.column("Date", width=150, anchor='center')
    tree.column("Time", width=150, anchor='center')
    tree.column("Reason", width=400, anchor='w')

    # Headings
    tree.heading("ID", text="ID")
    tree.heading("Patient", text="Patient")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Reason", text="Reason")

    # Scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Layout
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load data
    try:
        c.execute("SELECT * FROM appointments")
        appointments = c.fetchall()
        if not appointments:
            messagebox.showinfo("No Records", "No appointments found")
            view_window.destroy()
            return
        
        for appointment in appointments:
            tree.insert("", "end", values=appointment)
            
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        view_window.destroy()


# main gui
window = Tk()
window.geometry("1100x733")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 733,
    width = 1100,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
canvas.create_rectangle(487.0, 0.0, 1100.0, 733.0, fill=BG_COLOR, outline="")

canvas.create_text(569.0, 98.0, anchor="nw", text="DOCTOR’S DASHBOARD", fill="#FFFFFF", font=("Inter Bold", 40 * -1))

# buttons
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=view_patients, relief="flat")
button_1.place(x=578.0, y=312.0, width=446.0, height=55.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=view_appointments, relief="flat")
button_2.place(x=578.0, y=512.0, width=446.0, height=55.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(image=button_image_3, borderwidth=0, highlightthickness=0, command=add_appointment, relief="flat")
button_3.place(x=578.0, y=412.0, width=446.0, height=55.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(image=button_image_4, borderwidth=0, highlightthickness=0, command=add_patient, relief="flat")
button_4.place(x=578.0, y=210.0, width=446.0, height=55.0)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(image=button_image_5, borderwidth=0, highlightthickness=0, command=window.destroy, relief="flat")
button_5.place(x=697.0, y=614.0, width=208.0, height=70.0)

# Images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(243.0, 366.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(225.0, 171.0, image=image_image_2)

window.mainloop()