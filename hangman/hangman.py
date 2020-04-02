import random

done = False
isWon = False
isLost = False

current_unknown = {
    # counter for player guesses
    "guesses":0,
    "max_guesses":7,
    # the current word the player has to guess
    "word": [],
    # the known parts of the current word
    "known_word": [],
    "word_length": 0,
    "letters_known": 0
}

def get_random_word():
    words = ['rain', 'green tree', 'hunter', 'wide road', 'basement', 'fast car', 'luck', 'slow car', 'yellow sign']
    index = random.randint(0, len(words) - 1)
    return words[index]

def print_masked_character(x):
    print(f"x is {x} and y is {y}")
    if x == y:
        return x
    elif y == " ":
        return " "
    else:
        return "_"

# returns a list of boolean values for each index in source_list
# spaces are true everything else is false
def mask_word(source_list):
    masked_word = [False] * len(source_list)
    masked_word = list(map(lambda x: x == " ", source_list))
    return masked_word

def mask_or_reveal(x, y):
    if x:
        return y
    else:
        return "_"

def reset_current_unknown(current_unknown):
    current_unknown["guesses"] = 0
    current_unknown["max_guesses"] = 6
    current_unknown["word"] = list(get_random_word())
    current_unknown["known_word"] = mask_word(current_unknown["word"])
    current_unknown["word_length"] = len(current_unknown["word"])
    current_unknown["letters_known"] = current_unknown["known_word"].count(True)

def update_known_letters(current_unknown):
    current_unknown["letters_known"] = current_unknown["known_word"].count(True)

def increase_bad_guesses(current_unknown):
    current_unknown["guesses"] += 1

def init_game(current_unknown):
    reset_current_unknown(current_unknown)

def print_known_word(current_unknown):
    result = list(map(mask_or_reveal, current_unknown["known_word"], current_unknown["word"]))
    print("".join(result))

def check_win_condition(current_unknown):
    if current_unknown["letters_known"] == current_unknown["word_length"]:
        return True
    else:
        return False

def check_lose_condition(current_unknown):
    if current_unknown["guesses"] >= current_unknown["max_guesses"]:
        return True

def get_user_letter():
    return  input("Guess a letter: ")

def check_input_against_word(current_unknown, user_input):
    good_guess = False
    if len(user_input) == 1:
        input_letter = user_input.strip()
    # check first if the letter is in word
        if input_letter in current_unknown["word"]:
        # if it is, then check if that letter has already being guessed
            word = current_unknown["word"]
            known_word = current_unknown["known_word"]
            for index in range(len(word)):
                if word[index] == input_letter:
                    if known_word[index] == False:
                        known_word[index] = True
                        good_guess = True
                        update_known_letters(current_unknown)
            # if so, bad guess
    elif len(user_input) == current_unknown["word_length"]:
        if list(user_input) == current_unknown["word"]:
            # current_unknown["known_word"] = [True] * current_unknown["word_length"]
            current_unknown["letters_known"] = current_unknown["word_length"]
            good_guess = True
        # otherwise good guess
    current_unknown["known_word"].count(True)
    return good_guess
    # letter is not in word, bad guess

def want_to_play_again():
    user_input = input("Do you want to play another round? (yes/no) ")
    if 'y' in user_input:
        return False
    else:
        return True

def draw_hangman(number):
    hangman = [
        "",
        " ____\n|    |\n|    0\n|\n|\n|\n-",
        " ____\n|    |\n|    0\n|    |\n|\n|\n-",
        " ____\n|    |\n|    0\n|   -|\n|\n|\n-",
        " ____\n|    |\n|    0\n|   -|-\n|\n|\n-",
        " ____\n|    |\n|    0\n|   -|-\n|   / \n|\n-",
        " ____\n|    |\n|    0\n|   -|-\n|   / \\\n|\n-",
    ]
    print(hangman[number])

# initialize game
init_game(current_unknown)

# game loop
while not done:
    good_guess = False
    
    # print what is known about the current word   
    print_known_word(current_unknown)
    
    # get input
    user_input = get_user_letter()
    
    # check input against word
    good_guess = check_input_against_word(current_unknown, user_input)
    if good_guess:
        print("Good guess")
    else: 
        increase_bad_guesses(current_unknown)
        draw_hangman(current_unknown["guesses"])
    
    # check winning condition 
    isWon = check_win_condition(current_unknown)
    # if won set done to True
    if isWon:
        print("You won")
        done = True
    
    # check if game is lost
    isLost = check_lose_condition(current_unknown)
    # if lost set done to True
    if isLost:
        print("You lost")
        looking_for = "".join(current_unknown["word"])
        print(f"The correct word was \"{looking_for}\"")
        done = True
    
    # if done ask if player wants to play again
    if done:
        done = want_to_play_again()
        if not done:
            reset_current_unknown(current_unknown)