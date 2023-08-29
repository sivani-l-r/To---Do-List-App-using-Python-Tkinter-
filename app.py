import tkinter as tk
from tkinter import simpledialog

class TODOGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO List")
        self.root.geometry("400x500")  # Adjusted window size
        
         # Color Palette (Pastel Colors)
        self.bg_color = "#F0F4F8"
        self.button_color = "#AEB6BF"
        self.text_color = "#333333"

        self.tasks = []

        # Heading
        self.heading_label = tk.Label(root, text="TO - DO List", font=("Helvetica", 24, "bold"), fg=self.text_color, bg=self.bg_color)
        self.heading_label.pack(pady=10)

        # Prompt Label
        self.prompt_label = tk.Label(root, text="Enter a task:", font=("Helvetica", 12), fg=self.text_color, bg=self.bg_color)
        self.prompt_label.pack(pady=5)

        self.task_entry = tk.Entry(root, font=("Helvetica", 12))
        self.task_entry.pack(pady=5, padx=20, fill=tk.X)

        # Priority List
        self.priority_label = tk.Label(root, text="Select Priority", font=("Helvetica", 12), fg=self.text_color, bg=self.bg_color)
        self.priority_label.pack(pady=5, anchor=tk.W, padx=20)

        self.priority_var = tk.StringVar(root)
        self.priority_var.set("Low")
        self.priority_menu = tk.OptionMenu(root, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.config(font=("Helvetica", 12), bg=self.button_color)
        self.priority_menu.pack(pady=5, padx=20, fill=tk.X)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg=self.button_color)
        self.add_button.pack(pady=5, padx=20, fill=tk.X)
        
        # Scrollable Frame
        self.frame1 = tk.Frame(root)
        self.frame1.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.task_list = tk.Listbox(self.frame1, bg=self.bg_color, selectbackground=self.button_color, selectmode=tk.SINGLE, font=("Helvetica", 12), height=3)
        self.task_list.pack(side=tk.TOP, padx=20, pady=(0, 5), fill=tk.BOTH, expand=True)

        self.task_scrollbar = tk.Scrollbar(self.frame1)
        self.task_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=self.task_scrollbar.set)
        self.task_scrollbar.config(command=self.task_list.yview)

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=(0, 10))

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_task, bg=self.button_color)
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_task, bg=self.button_color)
        self.clear_button = tk.Button(button_frame,command=self.clear_task , text="Clear All", bg=self.button_color)
        self.save_button = tk.Button(button_frame,command=self.save_task , text="Save", bg=self.button_color)
        self.load_button = tk.Button(button_frame,command=self.load_task , text="Load", bg=self.button_color)

        self.edit_button.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.load_button.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task:
            task_with_priority = f"[{priority}] {task}"
            self.tasks.append(task_with_priority)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
            


    def edit_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            edited_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=selected_task)
            if edited_task:
                self.tasks[selected_index[0]] = edited_task
                self.update_task_list()

    def delete_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.update_task_list()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task_info in self.tasks:
            task_text = task_info["task"]
            completed = task_info["completed"]
            checkbox = "☑" if completed else "☐"
            self.task_list.insert(tk.END, f"{checkbox} {task_text}")

    def toggle_task_completion(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.update_task_list()

            
    def clear_task(self):
        self.task_list.delete(0, tk.END)
        self.tasks = []  # Clear the tasks list as well


    def save_task(self):
        tasks = self.task_list.get(0, tk.END)
        with open("tasklist.txt", "w") as taskfile:
            for task in tasks:
                taskfile.write(task + "\n")

                
    def load_task(self):
        try:
            with open("tasklist.txt", "r") as taskfile:
                task_list = taskfile.readlines()
            
            self.task_list.delete(0, tk.END)  # Clear the existing task list
            for task in task_list:
                if task.strip():  # Make sure the task is not an empty line
                    self.task_list.insert(tk.END, task.strip())
        except FileNotFoundError:
            with open("tasklist.txt", "w"):
                pass  # Create an empty file if it doesn't exist        

if __name__ == "__main__":
    root = tk.Tk()
    app = TODOGUI(root)
    root.mainloop()


