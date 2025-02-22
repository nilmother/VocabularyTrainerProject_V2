import pandas as pd
from tkinter import *
from tkinter import ttk
import util

class App:

    def __init__(self, root):
        root.title("My First Vocabulary Trainer")
        root.minsize(1200, 400)
        root.geometry("600x400+50+50")
        root.bind("<Return>", self.check_answer)  # Bind Enter key to check answer

        self.file_name = "A1_Vocabulaire.xlsx"

        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.currentUnit = "ALL"
        self.current_word = ["", ""]  # Default empty list to avoid errors
        self.current_word_index = 0  # Start at -1 to trigger first word
        self.current_task_length = 0
        self.current_score = 0
        
        self.font_attributes = ("helvetica", 14, "bold")

        # StringVars for dynamic text updates
        self.info_line = StringVar(value="Salut Nils! Let's learn some French")
        self.question_line = StringVar(value="What do you want to learn?")
        self.stat_line = StringVar(value="This will be your SCORE")

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
        self.dropdown_tasks.bind("<<ComboboxSelected>>", self.set_task)

        # Dropdown for units
        self.dropdown_unit_var = StringVar(value="ALL")
        unit_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "ALL"]
        self.dropdown_units = ttk.Combobox(root, textvariable=self.dropdown_unit_var, values=unit_options, state="readonly")
        self.dropdown_units.place(y=90, x=10)
        self.dropdown_units.bind("<<ComboboxSelected>>", self.set_unit)

        # Restart Button
        self.restart_button = Button(root, text="Restart", font=self.font_attributes, command=self.restart, width=10, height=1)
        self.restart_button.place(x=10, y=10)
        
    def load_words(self, task_name):
        try:
            self.task_name = task_name
            self.df = pd.read_excel(self.file_name, sheet_name=task_name)
            self.df = self.df.dropna()  # Drop rows with NaN values
            
            self.df = self.df.sample(frac=1).reset_index(drop=True)
            self.df["learnt_correct"] = False
        
            if self.df.empty:
                self.info_line.set(f"No valid data found in {task_name}.")
                return None
        
            self.set_unit()   
                        
            # Update the stat_line based on the filtered DataFrame
            self.info_line.set(f"Now learning {self.task_name}.")
            self.current_task_length = len(self.filtered_df)      
            
            self.show_exercise(task_name, self.current_word_index)
                    
        except Exception as e:
            self.info_line.set(f"Error loading task: {e}")
            
            
    def set_task(self, event):
        task_name = self.dropdown_task_var.get()
        self.load_words(task_name)
        self.current_task_length = len(self.filtered_df)

            
            
    def set_unit(self, event=None):
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
                self.question_line.set("none")
            else:
                self.stat_line.set(f"Unit {self.currentUnit}: You have {self.current_score} from {len(self.filtered_df)} words correct.")
            
            # Call show_exercise again to display the next item
            self.current_word_index = 0
            self.show_exercise(self.task_name, self.current_word_index)
                
        except ValueError as ve:
            self.question_line.set(f"NO EXERCISES LOADED value error")
        except KeyError as ke:
            self.question_line.set(f"NO EXERSICES IN THIS UNIT key error")  
    
                                              
    def show_exercise(self, task_name, current_word_index):
                    
        if task_name == "les verbes":
            current_exercise = util.exercise_verbes(self.filtered_df, current_word_index)
        elif task_name == "les noms":
            current_exercise = util.exercise_noms(self.filtered_df, current_word_index)
        elif task_name == "les adjectifs":
            current_exercise = util.exercise_adjectifs(self.filtered_df, current_word_index)
        elif task_name == "les adverbs":
            current_exercise = util.exercise_adverbs(self.filtered_df, current_word_index)    
        elif task_name == "les prépositions":
            current_exercise = util.exercise_prep(self.filtered_df, current_word_index)
        elif task_name == "les phrases":
            current_exercise = util.exercise_phrases(self.filtered_df, current_word_index)
            
        else:
            current_exercise = None
            
        self.current_word = list(current_exercise) if current_exercise else ["No question", "No answer"]
        self.question_line.set(self.current_word[0])  # Show question 

        
        if self.current_word_index >= self.current_task_length:
            self.current_word_index = 0    

        
    def check_answer(self, event=None):
        user_answer = self.lbl_answer.get().strip()  # Get user input
        correct_answer = self.current_word[1]  # Correct answer from stored word

        if user_answer.lower() == correct_answer.lower():  # Case insensitive check
            self.info_line.set("✅ Correct!")
            self.current_score += 1
            self.stat_line.set(f"Unit {self.currentUnit}: You have {self.current_score} from {len(self.filtered_df)} words correct.")
            self.lbl_answer.delete(0, END)  # Clear input field
            self.filtered_df.loc[self.current_word_index, "learnt_correct"] = True
            self.current_word_index += 1
            self.show_exercise(self.task_name, self.current_word_index)  # Move to next word

            print(self.filtered_df.loc[self.current_word_index, "learnt_correct"])
        else:
            self.info_line.set(f"❌ the correct word is: {correct_answer}")
            self.lbl_answer.delete(0, END)
            self.current_word_index += 1
            self.show_exercise(self.task_name, self.current_word_index)

    def restart(self):
        self.question_line.set("What do you want to learn?")
        self.stat_line.set("This will be your SCORE")
        self.info_line.set("Salut Nils! Let's learn some French")
        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()
        self.dropdown_task_var.set("choose an exercise")
        self.dropdown_unit_var.set("ALL")
        self.lbl_answer.delete(0, END)
        self.current_score = 0
        self.current_word_index = 0
        
        
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
