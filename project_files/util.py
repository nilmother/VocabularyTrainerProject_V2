import pandas as pd
import unicodedata

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

def exercise_verbes(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_verb = current_dict["INFINITIF"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_verb]


def exercise_noms(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_nom = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    current_article = current_dict["ARTICLE"][current_int]
    current_answer = current_article + " " + current_nom
    return [current_translation, current_answer]


def exercise_adjectifs(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_adjectif = current_dict["DEUTSCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_adjectif]


def exercise_adverbs(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_adverb = current_dict["DEUTSCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_adverb]


def exercise_prep(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_prep = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    learnt_correct = current_dict["learnt_correct"][current_int]
    return [current_translation, current_prep, learnt_correct]


def exercise_phrases(df, index):
    current_dict = df.to_dict('list')
    current_int = index
    current_phrase = current_dict["FRENCH"][current_int] 
    current_translation = current_dict["DEUTSCH"][current_int]
    return [current_translation, current_phrase]



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
