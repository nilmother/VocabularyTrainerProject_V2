import pandas as pd
import random

file_name = "A1_Vocabulaire.xlsx"  # Replace with the path to your file

class myVocabulary:
    
    def load_data(self, task_name):
            df = pd.read_excel(file_name, sheet_name = task_name)
            df_reduced = df.dropna()  # Drop rows with NaN values
            print("Vocabulary loaded successfully!")
            
            if df_reduced.empty:
                print(f"No valid data found in {task_name}.")
                return None
            
            return df_reduced
        
    def get_word_from_index(self, df, current_int):
        current_dict = df.to_dict('list')
        current_word = current_dict["DEUTSCH"][current_int] 
        return  current_word
    
    def get_number_of_words(self, df):
        return len(df)
         
    def get_solution(self, df, current_int):
        current_dict = df.to_dict('list')
        current_solution = current_dict["FRENCH"][current_int] 
        return current_solution
         
task_name = input("what do you want to learn?")

myVoc = myVocabulary()
myWords = myVoc.load_data(task_name)

myWordsLength = myVoc.get_number_of_words(myWords)
myWordsOrder = [i for i in range(myWordsLength)]
random.seed(42)
random.shuffle(myWordsOrder)

myExercise = myVoc.get_word_from_index(myWords, myWordsOrder[4])
mySolution = myVoc.get_solution(myWords, myWordsOrder[4])

print(myExercise)
print(mySolution)


# Exercise loop
    
score = 0
for i in range(myWords):
        exercise_word = myVocabulary.get_word_from_index(myWords, i)
        solution_word = myVocabulary.get_solution(myWords, i)

        # Ask the user for translation
        print(f"[Word {i + 1}/{myWordsLength}] Translate this word into French: {exercise_word}")
        user_response = input("Your answer: ").strip()

        if user_response.lower() == solution_word.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is: {solution_word}")

        print("")

    # Display final score
print(f"Exercise complete! Your score: {score}/{myWordsLength}")
