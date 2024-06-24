import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, filedialog

student_data = []

def add_student():
    if id_var.get() == "" or name_var.get() == "" or gender_var.get() == "" or age_var.get() == "" or endate_var.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        student = [id_var.get(), name_var.get(), gender_var.get(), age_var.get(), endate_var.get(), 0.0] 
        student_data.append(student)
        update_table()
        clear()

def update_student():
    selected_item = student_table.selection()
    if selected_item:
        item_index = student_table.index(selected_item[0])
        student = [id_var.get(), name_var.get(), gender_var.get(), age_var.get(), endate_var.get(), student_data[item_index][5]]  
        student_data[item_index] = student
        update_table()
        clear()
    else:
        messagebox.showerror("Error", "No student selected")

def delete_student():
    selected_item = student_table.selection()
    if selected_item:
        item_index = student_table.index(selected_item[0])
        del student_data[item_index]
        update_table()
        clear()
        save_to_file()
    else:
        messagebox.showerror("Error", "No student selected")

def clear():
    id_var.set("")
    name_var.set("")
    gender_var.set("")
    age_var.set("")
    endate_var.set("")

def get_cursor(ev):
    cursor_row = student_table.focus()
    contents = student_table.item(cursor_row)
    row = contents['values']
    id_var.set(row[0])
    name_var.set(row[1])
    gender_var.set(row[2])
    age_var.set(row[3])
    endate_var.set(row[4])

def update_table():
    student_table.delete(*student_table.get_children())
    for row in student_data:
        student_table.insert('', 'end', values=row)

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            for student in student_data:
                for data in student:
                    file.write(f"{data}\n")
                file.write("---\n")
        messagebox.showinfo("Success", "Data saved successfully")

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            student_data.clear()
            student = []
            for line in file:
                line = line.strip()
                if line == "---":
                    student_data.append(student)
                    student = []
                else:
                    student.append(line)
        update_table()
        messagebox.showinfo("Success", "Data loaded successfully")

        # Display loaded data file
        show_loaded_data(file_path)

def show_loaded_data(file_path):
    with open(file_path, "r") as file:
        loaded_data = file.read()
    messagebox.showinfo("Loaded Data", f"Recorded data from file:\n\n{loaded_data}")

def calculate_gpa(total_score):
    if total_score >= 90:
        return 4.0
    elif total_score >= 80:
        return 3.0
    elif total_score >= 70:
        return 2.0
    elif total_score >= 60:
        return 1.0
    else:
        return 0.0

def calculate_total_marks(sessional, midterm, final):
    return sessional + midterm + final

def calculate():
    course_name = selected_course.get()
    sessional_marks = float(sessional_entry.get())
    midterm_marks = float(midterm_entry.get())
    final_marks = float(final_entry.get())

    total_marks = calculate_total_marks(sessional_marks, midterm_marks, final_marks)
    gpa = calculate_gpa(total_marks)

    courses[course_name] = {"sessional": sessional_marks, "midterm": midterm_marks, "final": final_marks, "gpa": gpa}

    update_gpa_table()
    update_cgpa_label()

def update_gpa_table():
    gpa_tree.delete(*gpa_tree.get_children())
    for course, data in courses.items():
        gpa_tree.insert("", "end", values=(course, data["gpa"]))

def update_cgpa_label():
    overall_cgpa = calculate_gpa(courses)
    cgpa_label.config(text=f"Overall CGPA: {overall_cgpa:.2f}")
    return overall_cgpa

def open_cgpa_window():
    overall_cgpa = update_cgpa_label()
    messagebox.showinfo("Overall CGPA", f"Overall CGPA: {overall_cgpa:.2f}")

def open_calculate_window():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected")
        return

    item_index = student_table.index(selected_item[0])
    student = student_data[item_index]

    new_window = Toplevel(root)
    new_window.title("GPA Calculator")
    new_window.geometry("450x500")
    new_window.configure(bg="#e1f2fb")

    global selected_course, sessional_entry, midterm_entry, final_entry, gpa_tree, cgpa_label, courses
    selected_course = tk.StringVar()

    courses = {
        "PF": {"sessional": 0, "midterm": 0, "final": 0, "gpa": 0},
        "CALCULUS": {"sessional": 0, "midterm": 0, "final": 0, "gpa": 0},
        "ICT": {"sessional": 0, "midterm": 0, "final": 0, "gpa": 0},
        "ENGLISH": {"sessional": 0, "midterm": 0, "final": 0, "gpa": 0},
        "M.FC": {"sessional": 0, "midterm": 0, "final": 0, "gpa": 0}
    }

    student_label = ttk.Label(new_window, text=f"Calculating GPA for: {student[1]}")
    student_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

    course_label = ttk.Label(new_window,  text="Select Course:")
    course_label.grid(row=1, column=0, padx=10, pady=5)

    course_dropdown = ttk.Combobox(new_window, textvariable=selected_course, values=list(courses.keys()))
    course_dropdown.grid(row=1, column=1, padx=10, pady=5)

    sessional_label = ttk.Label(new_window, text="Enter Sessional Marks (out of 40):")
    sessional_label.grid(row=2, column=0, padx=10, pady=5)
    sessional_entry = ttk.Entry(new_window)
    sessional_entry.grid(row=2, column=1, padx=10, pady=5)

    midterm_label = ttk.Label(new_window, text="Enter Midterm Marks (out of 20):")
    midterm_label.grid(row=3, column=0, padx=10, pady=5)
    midterm_entry = ttk.Entry(new_window)
    midterm_entry.grid(row=3, column=1, padx=10, pady=5)

    final_label = ttk.Label(new_window, text="Enter Final Marks (out of 100):")
    final_label.grid(row=4, column=0, padx=10, pady=5)
    final_entry = ttk.Entry(new_window)
    final_entry.grid(row=4, column=1, padx=10, pady=5)

    calculate_button = ttk.Button(new_window, text="Calculate GPA", command=calculate)
    calculate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    gpa_tree = ttk.Treeview(new_window, columns=("Course", "GPA"), show="headings")
    gpa_tree.heading("Course", text="Course")
    gpa_tree.heading("GPA", text="GPA")
    gpa_tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    cgpa_label = ttk.Label(new_window, text="Overall CGPA: ")
    cgpa_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Main window
root = tk.Tk()
root.title("Academic Hub")
root.geometry("1100x750")
root.configure(bg="#e1f2fb")

title = tk.Label(root, text="Academic Hub", bd=10, relief=tk.GROOVE, font=("times new roman", 40, "bold"), bg="cyan", fg="black")
title.pack(side=tk.TOP, fill=tk.X)

manage_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#e1f2fb")
manage_frame.place(x=20, y=100, width=500, height=550)

m_title = tk.Label(manage_frame, text="Manage Students", bg="#e1f2fb", fg="black", font=("times new roman", 30, "bold"))
m_title.grid(row=0, columnspan=2, pady=20)

lbl_id = tk.Label(manage_frame, text="ID", bg="#e1f2fb", fg="black", font=("times new roman", 20, "bold"))
lbl_id.grid(row=1, column=0, pady=10, padx=20, sticky="w")
id_var = tk.StringVar()
txt_id = tk.Entry(manage_frame, textvariable=id_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
txt_id.grid(row=1, column=1, pady=10, padx=20, sticky="w")

lbl_name = tk.Label(manage_frame, text="Name", bg="#e1f2fb", fg="black", font=("times new roman", 20, "bold"))
lbl_name.grid(row=2, column=0, pady=10, padx=20, sticky="w")
name_var = tk.StringVar()
txt_name = tk.Entry(manage_frame, textvariable=name_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
txt_name.grid(row=2, column=1, pady=10, padx=20, sticky="w")

lbl_gender = tk.Label(manage_frame, text="Gender", bg="#e1f2fb", fg="black", font=("times new roman", 20, "bold"))
lbl_gender.grid(row=3, column=0, pady=10, padx=20, sticky="w")
gender_var = tk.StringVar()
combo_gender = ttk.Combobox(manage_frame, textvariable=gender_var, font=("times new roman", 13, "bold"), state='readonly')
combo_gender['values'] = ("Male", "Female", "Other")
combo_gender.grid(row=3, column=1, pady=10, padx=20)

lbl_age = tk.Label(manage_frame, text="Age", bg="#e1f2fb", fg="black", font=("times new roman", 20, "bold"))
lbl_age.grid(row=4, column=0, pady=10, padx=20, sticky="w")
age_var = tk.StringVar()
txt_age = tk.Entry(manage_frame, textvariable=age_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
txt_age.grid(row=4, column=1, pady=10, padx=20, sticky="w")

lbl_endate = tk.Label(manage_frame, text="Enroll Date", bg="#e1f2fb", fg="black", font=("times new roman", 20, "bold"))
lbl_endate.grid(row=5, column=0, pady=10, padx=20, sticky="w")
endate_var = tk.StringVar()
txt_endate = tk.Entry(manage_frame, textvariable=endate_var, font=("times new roman", 15, "bold"), bd=5, relief=tk.GROOVE)
txt_endate.grid(row=5, column=1, pady=10, padx=20, sticky="w")

# Button Frame
btn_frame = tk.Frame(manage_frame, bd=4, relief=tk.RIDGE, bg="#e1f2fb")
btn_frame.place(x=15, y=400, width=450)

add_btn = tk.Button(btn_frame, text="Add", width=10, command=add_student)
add_btn.grid(row=0, column=0, padx=10, pady=10)
update_btn = tk.Button(btn_frame, text="Update", width=10, command=update_student)
update_btn.grid(row=0, column=1, padx=10, pady=10)
delete_btn = tk.Button(btn_frame, text="Delete", width=10, command=delete_student)
delete_btn.grid(row=0, column=2, padx=10, pady=10)
calculate_btn = tk.Button(btn_frame, text="Calculate", width=10, command=open_calculate_window)
calculate_btn.grid(row=0, column=3, padx=10, pady=10)

# Save and Open Buttons
save_btn = tk.Button(root, text="Save to File", width=15, command=save_to_file, bg="light blue")
save_btn.place(x=20, y=680)

open_btn = tk.Button(root, text="Open File", width=15, command=open_file, bg="light blue")
open_btn.place(x=200, y=680)

# Frame for table
table_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#e1f2fb")
table_frame.place(x=550, y=100, width=530, height=550)

scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

student_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Gender", "Age", "Enroll Date", "CGPA"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)

student_table.heading("ID", text="ID")
student_table.heading("Name", text="Name")
student_table.heading("Gender", text="Gender")
student_table.heading("Age", text="Age")
student_table.heading("Enroll Date", text="Enroll Date")
student_table.heading("CGPA", text="CGPA")

student_table['show'] = 'headings'

student_table.column("ID", width=100)
student_table.column("Name", width=100)
student_table.column("Gender", width=100)
student_table.column("Age", width=100)
student_table.column("Enroll Date", width=100)
student_table.column("CGPA", width=100)

student_table.pack(fill=tk.BOTH, expand=True)
student_table.bind("<ButtonRelease-1>", get_cursor)

root.mainloop()



