import pandas as pd
import random
import unicodedata
from voc_trainer import file_name

# for the functionality of les verbes

# def get_pronom(pronom):
#     pronom_dict = {
#         1:["1P.S", "Je", "Ich"],
#         2:["2P.S", "Tu", "Du"],
#         3:["3P.S.m", "Il", "Er"],
#         4:["3P.S.f", "Elle", "Sie"],
#         5:["3P.S.b", "On", "Man"],
#         6:["1P.P", "Nous", "Wir"],  
#         7:["2P.P", "Vous", "Ihr"],
#         8:["3P.P.m", "Ils", "Sie[pl.m]"],
#         9:["3P.P.f", "Elles", "Sie[pl.w]"],
#         }
#     return pronom_dict[pronom]


def load_file(task_name):
    try:
        df = pd.read_excel(file_name, sheet_name=task_name)
        df_reduced = df.dropna()  # Drop rows with NaN values
        print("Vocabulary loaded successfully!")
        
        if df_reduced.empty:
            print(f"No valid data found in {task_name}.")
            return None
        return df_reduced
    except Exception as e:
        print(f"Error loading file: {e}")
        return None




def exercise_verbes(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["INFINITIF"])-1)
    current_verb = current_dict["INFINITIF"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_verb]


def exercise_noms(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["DEUTSCH"])-1)
    current_nom = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    current_article = current_dict["ARTICLE"][current_int]
    current_answer = current_article + " " + current_nom
    return [current_translation, current_answer]


def exercise_adjectifs(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["DEUTSCH"])-1)
    current_adjectif = current_dict["DEUTSCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_adjectif]


def exercise_adverbs(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["DEUTSCH"])-1)
    current_adverb = current_dict["DEUTSCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_adverb]


def exercise_prep(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["DEUTSCH"])-1)
    current_prep = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_prep]


def exercise_phrases(df):
    current_dict = df.to_dict('list')
    current_int = random.randint(0, len(current_dict["DEUTSCH"])-1)
    current_phrase = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_phrase]


def create_exercise(df, task_name):
    if task_name == "les verbes":
        current_exercise = exercise_verbes(df)
    elif task_name == "les noms":
        current_exercise = exercise_noms(df)
    elif task_name == "les adjectifs":
        current_exercise = exercise_adjectifs(df)
    elif task_name == "les adverbs":
        current_exercise = exercise_adverbs(df)    
    elif task_name == "les prépositions":
        current_exercise = exercise_prep(df)
    elif task_name == "les phrases":
        current_exercise = exercise_phrases(df)
        
    else:
        current_exercise = None
        
    return current_exercise








# STUFF FOR VERBS


    # def show_next_exercise(self):
    #     # Ensure that current_pronom is set correctly
    #     pronom_index = random.randint(1, 9)
    #     self.current_pronom = util.get_pronom(pronom_index)  # Get the pronom using the updated function

    #     # Select a random verb for the exercise
    #     current_verb = random.choice(self.verb_list)
    #     current_translation = self.verbs_dict[current_verb]["Translation"]

    #     # Store the verb for checking answers later
    #     self.current_verb = current_verb

    #     # Update UI with exercise details
    #     self.answer_entry.pack()
    #     self.submit_button.pack()

    #     # Update the question with verb and translation
    #     self.question_line.set(f"[{self.current_pronom[1]}] [{current_translation}]")

    #     self.answer_entry.delete(0, END)  # Clear the answer entry for the next question
