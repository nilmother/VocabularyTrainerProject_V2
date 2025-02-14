import pandas as pd
from tkinter import *
from tkinter import ttk
import util

# Example usage
file_name = "A1_Vocabulaire.xlsx"  # Replace with the path to your file

class App:

    def __init__(self, root):
        root.title("My First Vocabulary Trainer")
        root.minsize(1200, 600)
        root.geometry("600x600+50+50")
        root.bind("<Return>", self.check_answer)  # Bind Enter key to check answer


        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.currentUnit = None
        self.current_word = ["", ""]  # Default empty list to avoid errors
        self.current_word_index = -1  # Start at -1 to trigger first word
        self.current_task_lenght = 0
        
        self.font_attributes = ("helvetica", 12, "bold")

        # StringVars for dynamic text updates
        self.info_line = StringVar(value="Salut Nils! Let's learn some French")
        self.question_line = StringVar(value="What do you want to learn?")
        self.stat_line = StringVar(value="This will be your stats")

        # Labels and Input Fields
        self.lbl_info = Label(root, textvariable=self.info_line, font=self.font_attributes, height=2)
        self.lbl_info.pack()

        self.lbl_question = Label(root, textvariable=self.question_line, font=self.font_attributes, height=2, bg="yellow")
        self.lbl_question.pack()

        self.lbl_answer = Entry(root, font=self.font_attributes)
        self.lbl_answer.pack(padx=10, pady=10)

        self.lbl_stats = Label(root, textvariable=self.stat_line, font=self.font_attributes, height=2)
        self.lbl_stats.place(y=300, x=10)

        # Dropdown for tasks
        self.dropdown_task_var = StringVar(value="choose an exercise")
        task_options = ["les verbes", "les noms", "les adjectifs", "les adverbs", "les prépositions", "les phrases"]
        self.dropdown_tasks = ttk.Combobox(root, textvariable=self.dropdown_task_var, values=task_options, state="readonly")
        self.dropdown_tasks.place(y=60, x=10)
        self.dropdown_tasks.bind("<<ComboboxSelected>>", self.change_task)

        # Dropdown for units
        self.dropdown_unit_var = StringVar(value="ALL")
        unit_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "ALL"]
        self.dropdown_units = ttk.Combobox(root, textvariable=self.dropdown_unit_var, values=unit_options, state="readonly")
        self.dropdown_units.place(y=90, x=10)
        self.dropdown_units.bind("<<ComboboxSelected>>", self.change_unit)

        # Restart Button
        self.restart_button = Button(root, text="Restart", font=self.font_attributes, command=self.restart, width=10, height=1)
        self.restart_button.place(x=10, y=10)
        
    def load_task(self, task_name):
        try:
            self.task_name = task_name
            self.df = util.load_file(self.task_name)

            # Filter for the current unit if it's set
            if self.currentUnit is not None and self.currentUnit != "ALL":
                if self.df.empty:
                    raise ValueError("Data is not loaded. Please select a task first.")
                if "UNIT" not in self.df.columns:
                    raise KeyError("The column 'UNIT' does not exist in the DataFrame.")
                    
                self.filtered_df = self.df[self.df["UNIT"] == self.currentUnit]
            else:
                self.filtered_df = self.df  # No filtering needed for "ALL"
            
            self.show_exercise(task_name)
            
            # Update the stat_line based on the filtered DataFrame
            self.info_line.set(f"Now learning {self.task_name}.")
            self.current_task_lenght = len(self.filtered_df)      
            self.stat_line.set(f"Unit {self.currentUnit or 'ALL'}: {self.current_task_lenght} vocables available.")
                    
        except Exception as e:
            self.info_line.set(f"Error loading task: {e}")
            
    def change_unit(self, event=None):
        try:
            selected_unit = self.dropdown_unit_var.get()
            
            if selected_unit == "ALL":
                self.currentUnit = "ALL"
                self.filtered_df = self.df  # No filtering needed for "ALL"
            else:
                self.currentUnit = int(selected_unit)
                
                if self.df.empty:
                    raise ValueError("Data is not loaded. Please select a task first.")
                if "UNIT" not in self.df.columns:
                    raise KeyError("The column 'UNIT' does not exist in the DataFrame.")
                
                self.filtered_df = self.df[self.df["UNIT"] == self.currentUnit]
            
            # Update the stat_line based on the filtered DataFrame
            if self.filtered_df.empty:
                self.stat_line.set(f"Unit {self.currentUnit}: No exercises found.")
            else:
                self.stat_line.set(f"Unit {self.currentUnit}: {len(self.filtered_df)} exercises available.")
            
            # Call show_exercise again to display the next item
            self.show_exercise(self.task_name)
                
        except ValueError as ve:
            self.question_line.set(f"NO EXERCISES IN THIS UNIT")
        except KeyError as ke:
            self.question_line.set(f"NO EXERSICES IN THIS UNIT")  

    def change_task(self, event):
        task_name = self.dropdown_task_var.get()
        if task_name in ["les verbes", "les noms", "les adjectifs", "les adverbs", "les prépositions", "les phrases"]:
            self.load_task(task_name)
        else:
            self.info_line.set("Error: Invalid task selection")
                                              
    def show_exercise(self, task_name):
        self.current_word = list(util.create_exercise(self.filtered_df, task_name))  # Store word
        self.question_line.set(self.current_word[0])  # Show question
        
    def check_answer(self, event=None):
        user_answer = self.lbl_answer.get().strip()  # Get user input
        correct_answer = self.current_word[1]  # Correct answer from stored word

        if user_answer.lower() == correct_answer.lower():  # Case insensitive check
            self.info_line.set("✅ Correct!")
            self.lbl_answer.delete(0, END)  # Clear input field
            self.show_exercise(self.task_name)  # Move to next word
        else:
            self.info_line.set(f"❌ the correct word is: {correct_answer}")
            self.lbl_answer.delete(0, END)
            self.show_exercise(self.task_name)

    def restart(self):
        self.question_line.set("What do you want to learn?")
        self.stat_line.set("This will be your df.stats")
        self.info_line.set("Salut Nils! Let's learn some French")
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.dropdown_task_var.set("choose an exercise")
        self.dropdown_unit_var.set("choose a unit")
        self.lbl_answer.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
