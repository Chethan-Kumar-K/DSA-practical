import tkinter as tk
from tkinter import messagebox, ttk


# =========================================================
# NODE
# =========================================================

class Node:

    def __init__(self, token, name, age, department, emergency=False):

        self.token = token
        self.name = name
        self.age = age
        self.department = department
        self.emergency = emergency
        self.next = None


# =========================================================
# LINKED QUEUE
# Each department has its own linked queue
# =========================================================

class DepartmentQueue:

    def __init__(self):

        self.front = None
        self.rear = None
        self.count = 0

    # -----------------------------------------------------
    # NORMAL ENQUEUE
    # -----------------------------------------------------

    def enqueue(self, new_node):

        # Empty queue
        if self.front is None:

            self.front = new_node
            self.rear = new_node
            self.count += 1

            return

        # Add at rear
        self.rear.next = new_node
        self.rear = new_node

        self.count += 1

    # -----------------------------------------------------
    # EMERGENCY ENQUEUE
    # -----------------------------------------------------

    def enqueue_emergency(self, new_node):

        # Empty queue
        if self.front is None:

            self.front = new_node
            self.rear = new_node
            self.count += 1

            return

        # If first patient is normal,
        # emergency patient becomes FRONT
        if not self.front.emergency:

            new_node.next = self.front
            self.front = new_node
            self.count += 1

            return

        # Find the last emergency patient
        current = self.front

        while (
            current.next is not None
            and current.next.emergency
        ):
            current = current.next

        # Insert after the last emergency
        new_node.next = current.next
        current.next = new_node

        # If inserted at end, update REAR
        if new_node.next is None:
            self.rear = new_node

        self.count += 1

    # -----------------------------------------------------
    # DEQUEUE
    # -----------------------------------------------------

    def dequeue(self):

        if self.front is None:
            return None

        removed = self.front

        self.front = self.front.next

        removed.next = None

        self.count -= 1

        # Queue became empty
        if self.front is None:
            self.rear = None

        return removed

    # -----------------------------------------------------
    # PEEK
    # -----------------------------------------------------

    def peek(self):

        return self.front

    # -----------------------------------------------------
    # IS EMPTY
    # -----------------------------------------------------

    def is_empty(self):

        return self.front is None

    # -----------------------------------------------------
    # GET ALL PATIENTS
    # -----------------------------------------------------

    def get_all(self):

        patients = []

        current = self.front

        while current is not None:

            patients.append(current)

            current = current.next

        return patients


# =========================================================
# SMARTCARE SYSTEM
# =========================================================

class SmartCareSystem:

    def __init__(self):

        self.departments = {

            "General Medicine": DepartmentQueue(),
            "Orthopaedics": DepartmentQueue(),
            "ENT": DepartmentQueue(),
            "Cardiology": DepartmentQueue(),
            "Dermatology": DepartmentQueue(),
            "Paediatrics": DepartmentQueue()

        }

        self.next_token = 101

    # -----------------------------------------------------
    # REGISTER PATIENT
    # -----------------------------------------------------

    def register_patient(
        self,
        name,
        age,
        department,
        emergency
    ):

        new_node = Node(
            self.next_token,
            name,
            age,
            department,
            emergency
        )

        queue = self.departments[department]

        if emergency:

            queue.enqueue_emergency(new_node)

        else:

            queue.enqueue(new_node)

        self.next_token += 1

        return new_node

    # -----------------------------------------------------
    # GET DEPARTMENT QUEUE
    # -----------------------------------------------------

    def get_queue(self, department):

        return self.departments[department]

    # -----------------------------------------------------
    # TOTAL PATIENTS
    # -----------------------------------------------------

    def total_patients(self):

        total = 0

        for queue in self.departments.values():

            total += queue.count

        return total

    # -----------------------------------------------------
    # CLEAR ALL QUEUES
    # -----------------------------------------------------

    def clear(self):

        for queue in self.departments.values():

            current = queue.front

            while current is not None:

                next_node = current.next

                current.next = None

                current = next_node

            queue.front = None
            queue.rear = None
            queue.count = 0


# =========================================================
# GUI
# =========================================================

class SmartCareApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "SmartCare Hospital - OPD Token System"
        )

        self.root.geometry(
            "1200x780"
        )

        self.root.minsize(
            1050,
            700
        )

        self.system = SmartCareSystem()

        self.create_gui()

        self.update_all()


    # =====================================================
    # GUI CREATION
    # =====================================================

    def create_gui(self):

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = tk.Frame(
            self.root,
            bg="#1976D2",
            height=80
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="SMARTCARE HOSPITAL",
            font=("Arial", 24, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(
            pady=(12, 0)
        )

        tk.Label(
            header,
            text="OPD Patient Token Management System",
            font=("Arial", 11),
            bg="#1976D2",
            fg="white"
        ).pack()


        # -------------------------------------------------
        # MAIN
        # -------------------------------------------------

        main = tk.Frame(
            self.root,
            padx=15,
            pady=15
        )

        main.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # LEFT - REGISTRATION
        # =================================================

        form = tk.LabelFrame(
            main,
            text=" Register Patient ",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )

        form.place(
            x=10,
            y=10,
            width=300,
            height=410
        )


        # Patient Name

        tk.Label(
            form,
            text="Patient Name:",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.name_entry = tk.Entry(
            form,
            font=("Arial", 11)
        )

        self.name_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        # Age

        tk.Label(
            form,
            text="Age:",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.age_entry = tk.Entry(
            form,
            font=("Arial", 11)
        )

        self.age_entry.pack(
            fill="x",
            pady=(5, 15)
        )


        # Department

        tk.Label(
            form,
            text="Department:",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )

        self.department_combo = ttk.Combobox(
            form,
            state="readonly",
            values=[
                "General Medicine",
                "Orthopaedics",
                "ENT",
                "Cardiology",
                "Dermatology",
                "Paediatrics"
            ],
            font=("Arial", 10)
        )

        self.department_combo.pack(
            fill="x",
            pady=(5, 15)
        )

        self.department_combo.current(0)


        # Emergency checkbox

        self.emergency_var = tk.BooleanVar(
            value=False
        )

        self.emergency_check = tk.Checkbutton(
            form,
            text="🚨 Emergency Patient",
            variable=self.emergency_var,
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        self.emergency_check.pack(
            fill="x",
            pady=(5, 20)
        )


        # Register

        tk.Button(
            form,
            text="REGISTER PATIENT",
            command=self.register_patient,
            font=("Arial", 10, "bold"),
            bg="#2E7D32",
            fg="white",
            pady=10,
            cursor="hand2"
        ).pack(
            fill="x"
        )


        # =================================================
        # RIGHT - DEPARTMENT QUEUE
        # =================================================

        queue_frame = tk.LabelFrame(
            main,
            text=" Department Queue ",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        queue_frame.place(
            x=330,
            y=10,
            width=840,
            height=410
        )


        # Department selector

        tk.Label(
            queue_frame,
            text="Select Department:",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w"
        )


        self.view_department = ttk.Combobox(
            queue_frame,
            state="readonly",
            values=list(
                self.system.departments.keys()
            ),
            font=("Arial", 10)
        )

        self.view_department.pack(
            fill="x",
            pady=(5, 10)
        )

        self.view_department.current(0)

        self.view_department.bind(
            "<<ComboboxSelected>>",
            lambda event: self.update_department_view()
        )


        # Queue status

        self.queue_status = tk.Label(
            queue_frame,
            text="",
            font=("Arial", 11, "bold")
        )

        self.queue_status.pack(
            pady=5
        )


        # Queue canvas

        self.queue_canvas = tk.Canvas(
            queue_frame,
            width=790,
            height=190,
            bg="#F5F5F5",
            highlightthickness=1,
            highlightbackground="#CCCCCC"
        )

        self.queue_canvas.pack(
            pady=10
        )


        self.front_label = tk.Label(
            queue_frame,
            text="FRONT → None",
            font=("Arial", 10, "bold")
        )

        self.front_label.pack()


        self.rear_label = tk.Label(
            queue_frame,
            text="REAR → None",
            font=("Arial", 10, "bold")
        )

        self.rear_label.pack()


        # =================================================
        # BUTTONS
        # =================================================

        button_frame = tk.Frame(
            main
        )

        button_frame.place(
            x=10,
            y=440,
            width=1160,
            height=60
        )


        buttons = [

            ("CALL NEXT", self.call_next),

            ("PEEK", self.peek),

            ("DISPLAY QUEUE", self.display_queue),

            ("ALL DEPARTMENTS", self.show_all_departments),

            ("CLEAR", self.clear_queue)

        ]


        for i, (text, command) in enumerate(buttons):

            tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Arial", 10, "bold"),
                width=20,
                pady=8,
                cursor="hand2"
            ).grid(
                row=0,
                column=i,
                padx=5
            )


        # =================================================
        # INFORMATION TABLE
        # =================================================

        info_frame = tk.LabelFrame(
            main,
            text=" Queue Information ",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )

        info_frame.place(
            x=10,
            y=510,
            width=1160,
            height=170
        )


        columns = (

            "Position",
            "Token",
            "Patient",
            "Age",
            "Department",
            "Priority"

        )


        self.table = ttk.Treeview(
            info_frame,
            columns=columns,
            show="headings",
            height=5
        )


        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=175,
                anchor="center"
            )


        self.table.pack(
            fill="both",
            expand=True
        )


        # =================================================
        # STATUS
        # =================================================

        self.status = tk.Label(
            main,
            text="Total Patients: 0",
            font=("Arial", 11, "bold")
        )

        self.status.place(
            x=20,
            y=695
        )


    # =====================================================
    # REGISTER
    # =====================================================

    def register_patient(self):

        name = self.name_entry.get().strip()

        age_text = self.age_entry.get().strip()

        department = self.department_combo.get()

        emergency = self.emergency_var.get()


        # Validate name

        if not name:

            messagebox.showerror(
                "Invalid Input",
                "Please enter patient name."
            )

            return


        # Validate age

        try:

            age = int(age_text)

            if age <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Age must be greater than zero."
            )

            return


        # Register

        patient = self.system.register_patient(

            name,
            age,
            department,
            emergency

        )


        # Clear fields

        self.name_entry.delete(
            0,
            tk.END
        )

        self.age_entry.delete(
            0,
            tk.END
        )

        self.emergency_var.set(
            False
        )


        # Update GUI

        self.update_all()

        self.show_department_information()


        # Message

        priority = (
            "EMERGENCY"
            if emergency
            else "NORMAL"
        )


        messagebox.showinfo(

            "Patient Registered",

            f"Token {patient.token} issued.\n\n"
            f"Patient: {patient.name}\n"
            f"Department: {patient.department}\n"
            f"Priority: {priority}"

        )


    # =====================================================
    # CALL NEXT
    # =====================================================

    def call_next(self):

        department = self.view_department.get()

        queue = self.system.get_queue(
            department
        )


        patient = queue.dequeue()


        if patient is None:

            messagebox.showwarning(
                "Queue Empty",
                f"No patients waiting in {department}."
            )

            return


        self.update_all()

        self.show_department_information()


        messagebox.showinfo(

            "Now Calling",

            f"Now calling Token "
            f"{patient.token} – "
            f"{patient.name}\n\n"
            f"Department: {patient.department}"

        )


    # =====================================================
    # PEEK
    # =====================================================

    def peek(self):

        department = self.view_department.get()

        queue = self.system.get_queue(
            department
        )


        patient = queue.peek()


        self.clear_table()


        if patient is None:

            self.table.insert(

                "",
                "end",

                values=(

                    "-",
                    "-",
                    "No patients waiting",
                    "-",
                    department,
                    "-"

                )

            )

            return


        priority = (

            "🚨 EMERGENCY"
            if patient.emergency
            else "NORMAL"

        )


        self.table.insert(

            "",
            "end",

            values=(

                "NEXT",
                patient.token,
                patient.name,
                patient.age,
                patient.department,
                priority

            )

        )


    # =====================================================
    # DISPLAY SELECTED QUEUE
    # =====================================================

    def display_queue(self):

        self.show_department_information()


    # =====================================================
    # SHOW DEPARTMENT QUEUE
    # =====================================================

    def show_department_information(self):

        self.clear_table()


        department = self.view_department.get()

        queue = self.system.get_queue(
            department
        )


        patients = queue.get_all()


        for position, patient in enumerate(
            patients,
            start=1
        ):

            priority = (

                "🚨 EMERGENCY"
                if patient.emergency
                else "NORMAL"

            )


            self.table.insert(

                "",
                "end",

                values=(

                    position,
                    patient.token,
                    patient.name,
                    patient.age,
                    patient.department,
                    priority

                )

            )


    # =====================================================
    # SHOW ALL DEPARTMENTS
    # =====================================================

    def show_all_departments(self):

        self.clear_table()


        position = 1


        for department, queue in (
            self.system.departments.items()
        ):

            patients = queue.get_all()


            for patient in patients:

                priority = (

                    "🚨 EMERGENCY"
                    if patient.emergency
                    else "NORMAL"

                )


                self.table.insert(

                    "",
                    "end",

                    values=(

                        position,
                        patient.token,
                        patient.name,
                        patient.age,
                        patient.department,
                        priority

                    )

                )

                position += 1


    # =====================================================
    # CLEAR TABLE
    # =====================================================

    def clear_table(self):

        for item in self.table.get_children():

            self.table.delete(
                item
            )


    # =====================================================
    # UPDATE EVERYTHING
    # =====================================================

    def update_all(self):

        self.update_department_view()

        self.status.config(

            text=f"Total Patients: "
            f"{self.system.total_patients()}"

        )


    # =====================================================
    # UPDATE DEPARTMENT VISUALIZATION
    # =====================================================

    def update_department_view(self):

        department = self.view_department.get()


        if not department:

            return


        queue = self.system.get_queue(
            department
        )


        patients = queue.get_all()


        # Clear canvas

        self.queue_canvas.delete(
            "all"
        )


        # Status

        self.queue_status.config(

            text=(
                f"{department} — "
                f"{len(patients)} patient(s)"
            )

        )


        # Empty queue

        if not patients:

            self.front_label.config(
                text="FRONT → None"
            )

            self.rear_label.config(
                text="REAR → None"
            )

            return


        # FRONT

        self.front_label.config(

            text=(
                f"FRONT → Token "
                f"{queue.front.token} "
                f"({queue.front.name})"
            )

        )


        # REAR

        self.rear_label.config(

            text=(
                f"REAR → Token "
                f"{queue.rear.token} "
                f"({queue.rear.name})"
            )

        )


        # Draw nodes

        x = 20


        for index, patient in enumerate(
            patients
        ):

            # Emergency or normal

            label = (

                f"🚨 {patient.token}"
                if patient.emergency
                else f"{patient.token}"

            )


            self.queue_canvas.create_rectangle(

                x,
                50,
                x + 150,
                125,

                outline="#C62828"
                if patient.emergency
                else "#1976D2",

                width=3

            )


            self.queue_canvas.create_text(

                x + 75,
                72,

                text=label,

                font=("Arial", 10, "bold")

            )


            self.queue_canvas.create_text(

                x + 75,
                100,

                text=patient.name,

                font=("Arial", 10)

            )


            # Arrow

            if index < len(patients) - 1:

                self.queue_canvas.create_line(

                    x + 150,
                    87,

                    x + 180,
                    87,

                    arrow=tk.LAST,

                    width=2

                )


            x += 195


            if x > 730:

                break


        # Show table

        self.show_department_information()


    # =====================================================
    # CLEAR ALL QUEUES
    # =====================================================

    def clear_queue(self):

        if self.system.total_patients() == 0:

            messagebox.showinfo(

                "Queue",

                "All queues are already empty."

            )

            return


        confirm = messagebox.askyesno(

            "Clear Queues",

            "Remove all patients from all departments?"

        )


        if confirm:

            self.system.clear()

            self.clear_table()

            self.update_all()


            messagebox.showinfo(

                "Queues Cleared",

                "All remaining nodes have been released."

            )


    # =====================================================
    # EXIT
    # =====================================================

    def exit_program(self):

        self.system.clear()

        self.root.destroy()


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartCareApp(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.exit_program
    )

    root.mainloop()