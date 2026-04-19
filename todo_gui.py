import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlowTasks")
        self.root.configure(bg="#faf4ec")
        self.tasks = load_tasks()

        # Header
        header = tk.Frame(root, bg="#f7c087", height=8)
        header.pack(fill=tk.X, side=tk.TOP)
        header_label = tk.Label(root, text="Flow", fg="#e67c1e", bg="#faf4ec", font=("Segoe UI", 20, "bold"))
        header_label.place(x=30, y=20)
        header_label2 = tk.Label(root, text="Tasks", fg="#222", bg="#faf4ec", font=("Segoe UI", 20))
        header_label2.place(x=90, y=20)

        # Date
        today = datetime.now()
        day_str = today.strftime("%A")
        date_str = today.strftime("%d %B %Y")
        day_label = tk.Label(root, text=day_str.upper(), bg="#faf4ec", fg="#b87c3b", font=("Segoe UI", 10, "bold"))
        day_label.place(x=30, y=70)
        date_label = tk.Label(root, text=date_str, bg="#faf4ec", fg="#222", font=("Segoe UI", 18, "bold"))
        date_label.place(x=30, y=90)

        # Progress
        self.progress_label = tk.Label(root, text="", bg="#faf4ec", fg="#b87c3b", font=("Segoe UI", 10))
        self.progress_label.place(x=30, y=130)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
        self.progress.place(x=30, y=150)

        # Task List
        self.listbox = tk.Listbox(root, width=45, height=10, font=("Segoe UI", 12), bd=0, highlightthickness=0, selectbackground="#e67c1e", selectforeground="#fff")
        self.listbox.place(x=30, y=190)

        # Buttons
        style = ttk.Style()
        style.configure("Rounded.TButton", font=("Segoe UI", 10, "bold"), padding=6, relief="flat", borderwidth=0, background="#e67c1e", foreground="#fff")
        btn_frame = tk.Frame(root, bg="#faf4ec")
        btn_frame.place(x=30, y=420)

        ttk.Button(btn_frame, text="Add Task", style="Rounded.TButton", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Task", style="Rounded.TButton", command=self.update_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Completed", style="Rounded.TButton", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Task", style="Rounded.TButton", command=self.delete_task).pack(side=tk.LEFT, padx=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        self.listbox.delete(0, tk.END)
        completed = 0
        for idx, task in enumerate(self.tasks):
            status = "✓" if task["completed"] else " "
            display = f"[{status}] {task['title']}"
            self.listbox.insert(tk.END, display)
            if task["completed"]:
                completed += 1
        total = len(self.tasks)
        self.progress["maximum"] = total if total else 1
        self.progress["value"] = completed
        self.progress_label.config(text=f"Today's progress    {completed} / {total} done")

    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task description:")
        if title:
            self.tasks.append({"title": title, "completed": False})
            save_tasks(self.tasks)
            self.refresh_tasks()

    def update_task(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("No selection", "Select a task to update.")
            return
        new_title = simpledialog.askstring("Update Task", "Enter new description:")
        if new_title:
            self.tasks[idx[0]]["title"] = new_title
            save_tasks(self.tasks)
            self.refresh_tasks()

    def complete_task(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("No selection", "Select a task to mark as completed.")
            return
        self.tasks[idx[0]]["completed"] = True
        save_tasks(self.tasks)
        self.refresh_tasks()

    def delete_task(self):
        idx = self.listbox.curselection()
        if not idx:
            messagebox.showwarning("No selection", "Select a task to delete.")
            return
        del self.tasks[idx[0]]
        save_tasks(self.tasks)
        self.refresh_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.resizable(False, False)
    app = TodoApp(root)
    root.mainloop()