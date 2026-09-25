import tkinter as tk
from tkinter import messagebox, ttk


# ---------------------------------------------------------
# NODE CLASS
# ---------------------------------------------------------
class Node:
    def __init__(self, token, name, age, department):
        self.token = token
        self.name = name
        self.age = age
        self.department = department
        self.next = None


# ---------------------------------------------------------
# QUEUE CLASS - SINGLY LINKED LIST
# ---------------------------------------------------------
class PatientQueue:

    def __init__(self):
        self.front = None
        self.rear = None
        self.count = 0
        self.next_token = 101

    # ENQUEUE
    def enqueue(self, name, age, department):
        new_node = Node(
            self.next_token,
            name,
            age,
            department
        )

        # First node
        if self.front is None:
            self.front = new_node
            self.rear = new_node

        # Add at rear
        else:
            self.rear.next = new_node
            self.rear = new_node

        self.next_token += 1
        self.count += 1

        return new_node

    # DEQUEUE
    def dequeue(self):

        if self.front is None:
            return None

        removed_node = self.front
        self.front = self.front.next

        self.count -= 1

        # Queue became empty
        if self.front is None:
            self.rear = None

        removed_node.next = None

        return removed_node

    # PEEK
    def peek(self):
        return self.front

    # IS EMPTY
    def is_empty(self):
        return self.front is None

    # COUNT
    def get_count(self):
        return self.count

    # DISPLAY
    def get_all_patients(self):

        patients = []
        current = self.front

        while current is not None:
            patients.append(current)
            current = current.next

        return patients

    # CLEAR QUEUE
    def clear(self):

        current = self.front

        while current is not None:
            next_node = current.next
            current.next = None
            current = next_node

        self.front = None
        self.rear = None
        self.count = 0


# ---------------------------------------------------------
# GUI APPLICATION
# ---------------------------------------------------------
class SmartCareApp:

    def __init__(self, root):

        self.root = root
        self.root.title("SmartCare Hospital - OPD Token System")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        self.queue = PatientQueue()

        self.create_gui()
        self.update_display()

    # -----------------------------------------------------
    # CREATE GUI
    # -----------------------------------------------------
    def create_gui(self):

        # HEADER
        header = tk.Frame(
            self.root,
            bg="#1976D2",
            height=80
        )
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="SMARTCARE HOSPITAL",
            font=("Arial", 24, "bold"),
            bg="#1976D2",
            fg="white"
        )
        title.pack(pady=(12, 0))

        subtitle = tk.Label(
            header,
            text="OPD Patient Token Management System",
            font=("Arial", 11),
            bg="#1976D2",
            fg="white"
        )
        subtitle.pack()

        # MAIN FRAME
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        # -------------------------------------------------
        # LEFT SIDE - REGISTRATION
        # -------------------------------------------------

        form_frame = tk.LabelFrame(
            main,
            text=" Register Patient ",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        form_frame.place(
            x=10,
            y=10,
            width=320,
            height=360
        )

        # Name
        tk.Label(
            form_frame,
            text="Patient Name:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.name_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.name_entry.pack(fill="x", pady=(0, 12))

        # Age
        tk.Label(
            form_frame,
            text="Age:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.age_entry = tk.Entry(
            form_frame,
            font=("Arial", 11)
        )
        self.age_entry.pack(fill="x", pady=(0, 12))

        # Department
        tk.Label(
            form_frame,
            text="Department:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(5, 3))

        self.department_combo = ttk.Combobox(
            form_frame,
            values=[
                "General Medicine",
                "Orthopaedics",
                "ENT",
                "Cardiology",
                "Dermatology",
                "Paediatrics"
            ],
            state="readonly",
            font=("Arial", 10)
        )
        self.department_combo.pack(fill="x", pady=(0, 20))
        self.department_combo.current(0)

        # ENQUEUE BUTTON
        tk.Button(
            form_frame,
            text="➕ REGISTER PATIENT",
            command=self.register_patient,
            font=("Arial", 10, "bold"),
            bg="#2E7D32",
            fg="white",
            padx=10,
            pady=8,
            cursor="hand2"
        ).pack(fill="x")

        # -------------------------------------------------
        # MIDDLE - QUEUE VISUALIZATION
        # -------------------------------------------------

        queue_frame = tk.LabelFrame(
            main,
            text=" Patient Queue ",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        queue_frame.place(
            x=350,
            y=10,
            width=720,
            height=360
        )

        # Queue status
        self.status_label = tk.Label(
            queue_frame,
            text="Queue is empty",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(pady=5)

        # Queue visualization
        self.queue_canvas = tk.Canvas(
            queue_frame,
            width=680,
            height=180,
            bg="#F5F5F5",
            highlightthickness=1,
            highlightbackground="#CCCCCC"
        )
        self.queue_canvas.pack(pady=10)

        # FRONT / REAR indicators
        self.front_label = tk.Label(
            queue_frame,
            text="FRONT → No patient",
            font=("Arial", 10, "bold")
        )
        self.front_label.pack()

        self.rear_label = tk.Label(
            queue_frame,
            text="REAR → No patient",
            font=("Arial", 10, "bold")
        )
        self.rear_label.pack()

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_frame = tk.Frame(main)
        button_frame.place(
            x=10,
            y=390,
            width=1060,
            height=70
        )

        tk.Button(
            button_frame,
            text="📞 CALL NEXT",
            command=self.call_next,
            font=("Arial", 10, "bold"),
            bg="#C62828",
            fg="white",
            width=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="👁️ PEEK",
            command=self.peek_patient,
            font=("Arial", 10, "bold"),
            width=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="📋 DISPLAY",
            command=self.display_patients,
            font=("Arial", 10, "bold"),
            width=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            button_frame,
            text="⏱️ WAIT TIMES",
            command=self.show_wait_times,
            font=("Arial", 10, "bold"),
            width=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            button_frame,
            text="🗑️ CLEAR",
            command=self.clear_queue,
            font=("Arial", 10, "bold"),
            width=18,
            pady=8,
            cursor="hand2"
        ).grid(row=0, column=4, padx=5)

        # -------------------------------------------------
        # BOTTOM STATUS
        # -------------------------------------------------

        bottom_frame = tk.LabelFrame(
            main,
            text=" Queue Information ",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=10
        )
        bottom_frame.place(
            x=10,
            y=475,
            width=1060,
            height=100
        )

        self.count_label = tk.Label(
            bottom_frame,
            text="Patients Waiting: 0",
            font=("Arial", 12, "bold")
        )
        self.count_label.grid(
            row=0,
            column=0,
            padx=30,
            pady=10
        )

        self.empty_label = tk.Label(
            bottom_frame,
            text="Queue Status: EMPTY",
            font=("Arial", 12, "bold")
        )
        self.empty_label.grid(
            row=0,
            column=1,
            padx=30
        )

        self.token_label = tk.Label(
            bottom_frame,
            text="Next Token: 101",
            font=("Arial", 12, "bold")
        )
        self.token_label.grid(
            row=0,
            column=2,
            padx=30
        )

        self.wait_label = tk.Label(
            bottom_frame,
            text="Estimated Last Wait: 0 minutes",
            font=("Arial", 12, "bold")
        )
        self.wait_label.grid(
            row=0,
            column=3,
            padx=30
        )

    # -----------------------------------------------------
    # REGISTER PATIENT - ENQUEUE
    # -----------------------------------------------------
    def register_patient(self):

        name = self.name_entry.get().strip()
        age_text = self.age_entry.get().strip()
        department = self.department_combo.get()

        # Validate name
        if not name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter the patient's name."
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
                "Age must be a positive number."
            )
            return

        # ENQUEUE
        patient = self.queue.enqueue(
            name,
            age,
            department
        )

        messagebox.showinfo(
            "Patient Registered",
            f"Token {patient.token} issued.\n\n"
            f"Patient: {patient.name}\n"
            f"Department: {patient.department}"
        )

        # Clear input fields
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)

        self.update_display()

    # -----------------------------------------------------
    # DEQUEUE
    # -----------------------------------------------------
    def call_next(self):

        patient = self.queue.dequeue()

        if patient is None:
            messagebox.showwarning(
                "Queue Underflow",
                "No patients waiting."
            )
            return

        messagebox.showinfo(
            "Now Calling",
            f"Now calling Token {patient.token} – "
            f"{patient.name}\n\n"
            f"Department: {patient.department}"
        )

        self.update_display()

    # -----------------------------------------------------
    # PEEK
    # -----------------------------------------------------
    def peek_patient(self):

        patient = self.queue.peek()

        if patient is None:
            messagebox.showwarning(
                "Queue Empty",
                "No patients waiting."
            )
            return

        messagebox.showinfo(
            "Next Patient",
            f"Token: {patient.token}\n"
            f"Name: {patient.name}\n"
            f"Age: {patient.age}\n"
            f"Department: {patient.department}\n\n"
            f"This patient will be called next."
        )

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------
    def display_patients(self):

        patients = self.queue.get_all_patients()

        if not patients:
            messagebox.showinfo(
                "Waiting List",
                "No patients waiting."
            )
            return

        window = tk.Toplevel(self.root)
        window.title("SmartCare - Waiting List")
        window.geometry("800x400")

        tk.Label(
            window,
            text="Current Waiting List",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        columns = (
            "Token",
            "Name",
            "Age",
            "Department"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=150)

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        for patient in patients:
            tree.insert(
                "",
                "end",
                values=(
                    patient.token,
                    patient.name,
                    patient.age,
                    patient.department
                )
            )

    # -----------------------------------------------------
    # SELF-LEARNING FEATURE
    # ESTIMATED WAITING TIME
    # -----------------------------------------------------
    def show_wait_times(self):

        patients = self.queue.get_all_patients()

        if not patients:
            messagebox.showinfo(
                "Waiting Time",
                "No patients waiting."
            )
            return

        window = tk.Toplevel(self.root)
        window.title("Estimated Waiting Time")
        window.geometry("850x400")

        tk.Label(
            window,
            text="Estimated Patient Waiting Time",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(
            window,
            text="Assumption: 7 minutes per consultation",
            font=("Arial", 10)
        ).pack()

        columns = (
            "Position",
            "Token",
            "Patient",
            "Department",
            "Estimated Wait"
        )

        tree = ttk.Treeview(
            window,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=150)

        tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        for position, patient in enumerate(patients):

            wait_time = position * 7

            tree.insert(
                "",
                "end",
                values=(
                    position + 1,
                    patient.token,
                    patient.name,
                    patient.department,
                    f"{wait_time} minutes"
                )
            )

    # -----------------------------------------------------
    # CLEAR QUEUE
    # -----------------------------------------------------
    def clear_queue(self):

        if self.queue.is_empty():
            messagebox.showinfo(
                "Queue",
                "Queue is already empty."
            )
            return

        answer = messagebox.askyesno(
            "Clear Queue",
            "Are you sure you want to remove all waiting patients?"
        )

        if answer:

            self.queue.clear()

            messagebox.showinfo(
                "Queue Cleared",
                "All remaining nodes have been released."
            )

            self.update_display()

    # -----------------------------------------------------
    # UPDATE GUI
    # -----------------------------------------------------
    def update_display(self):

        self.queue_canvas.delete("all")

        patients = self.queue.get_all_patients()

        # Draw queue nodes
        x = 20

        for i, patient in enumerate(patients):

            # Node
            self.queue_canvas.create_rectangle(
                x,
                55,
                x + 140,
                125,
                outline="#1976D2",
                width=2
            )

            self.queue_canvas.create_text(
                x + 70,
                75,
                text=f"Token {patient.token}",
                font=("Arial", 10, "bold")
            )

            self.queue_canvas.create_text(
                x + 70,
                100,
                text=patient.name,
                font=("Arial", 10)
            )

            # Arrow to next node
            if i < len(patients) - 1:

                self.queue_canvas.create_line(
                    x + 140,
                    90,
                    x + 165,
                    90,
                    arrow=tk.LAST,
                    width=2
                )

            x += 180

            # Prevent drawing outside canvas
            if x > 620:
                break

        # Status
        if self.queue.is_empty():

            self.status_label.config(
                text="Queue is EMPTY"
            )

            self.front_label.config(
                text="FRONT → None"
            )

            self.rear_label.config(
                text="REAR → None"
            )

            self.empty_label.config(
                text="Queue Status: EMPTY"
            )

        else:

            self.status_label.config(
                text=f"{self.queue.count} patient(s) waiting"
            )

            self.front_label.config(
                text=f"FRONT → Token {self.queue.front.token} "
                     f"({self.queue.front.name})"
            )

            self.rear_label.config(
                text=f"REAR → Token {self.queue.rear.token} "
                     f"({self.queue.rear.name})"
            )

            self.empty_label.config(
                text="Queue Status: NOT EMPTY"
            )

        # Count
        self.count_label.config(
            text=f"Patients Waiting: {self.queue.count}"
        )

        # Next token
        self.token_label.config(
            text=f"Next Token: {self.queue.next_token}"
        )

        # Estimated last waiting time
        if self.queue.count > 0:

            last_wait = (self.queue.count - 1) * 7

        else:

            last_wait = 0

        self.wait_label.config(
            text=f"Estimated Last Wait: {last_wait} minutes"
        )


# ---------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartCareApp(root)

    root.mainloop()