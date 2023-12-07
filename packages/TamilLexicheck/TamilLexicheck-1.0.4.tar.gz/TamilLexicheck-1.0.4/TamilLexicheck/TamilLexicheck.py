
import pickle
import os

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]
file_path = os.path.join('C:\\Users\\raamk\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\TamilLexicheck', 'words.pickle')
# Read the contents of the file
with open(file_path, 'rb+') as tamil_words:
 tamil_word=pickle.load(tamil_words)

def spell_check(n):
    input_name=n
    threshold = 4
    closest_word = None
    min_distance = 4
    for word in tamil_word:
        distance = levenshtein_distance(word, input_name)

        if distance < min_distance:
            min_distance = distance
            closest_word = word
    print(closest_word)


if __name__=='__main__':
    try:
     word = input("Enter word to spell check: ")
     result = spell_check(word)
     print(f"Closest word found: {result}")
    except:
        print("No word is given as input")

