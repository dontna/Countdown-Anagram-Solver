import sys, requests

def remove_useless_words(letters: str, word_list: list):
    print("Removing words that can't be used...")

    words_list_cleaned = []
    letters_list = []
    no_dupe_letters_list = []

    letter_count = []
    potential_words = []

    # Remove any words, which use letters that are not in the letters.
    for word in word_list:
        bad_letter = False
        for x in word:
            if x not in letters:
                bad_letter = True
                break
        if not bad_letter:
            words_list_cleaned.append(word)

    for letter in letters:
        letters_list.append(letter)

    no_dupe_letters_list = list(set(letters_list))

    for letter in no_dupe_letters_list:
        letter_count.append(letters.count(letter))

    len_no_dupe_letters_list = len(no_dupe_letters_list)

    for word in words_list_cleaned:
        for letter in no_dupe_letters_list:
            times_in_word = word.count(letter)
            times_in_letters = letters.count(letter)

            if times_in_word > times_in_letters:
                break
            
            index = no_dupe_letters_list.index(letter)

            if index == len_no_dupe_letters_list - 1:
                potential_words.append(word)

    return potential_words

def get_best_word(letters: str):
    '''Return a word, made from the letters provided, which would also give the most points.'''

    with open("dictionary_new.txt", "r") as f:
        word_list = f.read().split('\n')

    potential_words = remove_useless_words(letters, word_list)
    potential_words.sort(key=len, reverse=True)

    # Get the best word
    best_word = ""
    other_words = []
    other_words_stopper = 6

    first_loop = True

    print("Checking for best valid word, this may take a few seconds...")
    for word in potential_words:
        if len(word) > len(best_word):
            if is_word_valid(word) == True:
                if first_loop:
                    first_loop = False
                else:
                    other_words.append(best_word)

                best_word = word
        else:
            other_words.append(word)


    print(f'Best Word: {best_word} ({len(best_word)} letters)')

    if len(other_words) > 0:
        print("\nYou also could've had:\n")
        for i,word in enumerate(other_words):
            if i == other_words_stopper:
                print(f"and {len(other_words) - i} more...")
                break
            else:
                print(f"{word} ({len(word)} letters)")
    else:
        print("and this is all we could find...")

def is_word_valid(word: str):
    '''Check word against the Merriam Webster dictionary, to ensure it could be used.'''
    r = requests.get(f"https://www.merriam-webster.com/dictionary/{word}", allow_redirects=False)

    if r.status_code == 200:
        return True
    else:
        return False

def check_only_letters(letters: str):
    '''Check to see if the string provided only contains letters in the English alphabet'''
    blacklist = ['!','"','£','$','%','^','&','*','(',')','_','+','=','-','0','9','8','7','6','5','4','3','2','1','[',']','#','\'',';',':','@','~','>','<','?','/','\.',',','\\','|','¬','`']
    
    for letter in letters:
        if letter in blacklist:
            return False
        
    return True

if __name__ == "__main__":

   if len(sys.argv) == 2:
       if len(sys.argv[1]) == 9:
           if check_only_letters(sys.argv[1]):
               get_best_word(sys.argv[1].lower())
           else:
               print("Please only use letters.")
               exit()
       else:
           print("Please enter the full 9 random letters.")
           exit()
   else:
       print("Please enter the random letters.")
       exit()
