# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
n = 10

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4,  
    'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 
    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 
    'y': 4, 'z': 10, '*' : 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    print("------------------------------------")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    
    lower_word = word.lower()
    wordlen = len(word)
    sum = 0
    score = 0

    #sum of the points for letters in the word
    if word == '':
        score = 0

    else:
        for elem in lower_word:
            sum += SCRABBLE_LETTER_VALUES[elem]



        
    #second component
    second = 7 * wordlen - 3 * (n-wordlen)
    if second > 1:
        score = second * sum
    else:
        score = sum * 1
        
    return score
    

# print (get_word_score("", 7))
     
        

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    display = ''
    for letter in hand.keys():
        for j in range(hand[letter]):
             display += letter + ' '      # print all on the same line
    return display                             # print an empty line
    
# hand = {'a':1,'p':2, 'l':1, 'e':1}
# print(display_hand(hand))

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        if i < num_vowels - 1:
            x = random.choice(VOWELS)
            hand[x] = hand.get(x, 0) + 1
        if i == num_vowels - 1:
            x = '*'
            hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
        
    
    return hand

# n = 9
# print (display_hand(deal_hand(n)))

#    
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    word_dic = get_frequency_dict(word.lower())

     
    new_hand = hand.copy()

    for key in word_dic:
        hand_num = new_hand.get(key, 0)
        word_num = word_dic[key]
        if word_num > hand_num:
            new_hand[key] = 0
        else:
            new_hand[key] = hand_num - word_num
     
    return new_hand

# hand = {'a':1,'p':2, 'l':1, 'e':1}
# word = 'appple'

# print(update_hand(hand, word))

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    word_dic = get_frequency_dict(word.lower())
    my_word = []
    my_hand = []
    new_hand = hand.copy()

    for i in word_dic:
        my_word.append(i) #create a list of letters in my word
        
    for i in hand:
        my_hand.append(i) #create a list of letters in my hand
 
    # wordlen = len(my_word) ####!!!
    in_hand = True
    word_lower = word.lower()
    
    vowels_count = 0
    if word_lower.find('*') != -1: #if my word contains * #1#
        for i in VOWELS:
            word_testing = word_lower.replace('*', i) #replace * with vowels one each time
            
            if word_testing in word_list: #if my word exists in wordlist
                vowels_count += 1 

                
                for i in range(len(my_word)): #test if I'm using letters from my hand
                    if  my_word[i] in my_hand: 
                        in_Hand = True
                    else:
                        in_Hand = False
                
                 
                if in_Hand == True: #if all letters used are in my hand
                    for key in word_dic: #test if I'm not overuse letters
                        hand_num = new_hand.get(key, 0)
                        word_num = word_dic[key]
                        if word_num > hand_num: #overuse letters
                            decision = False #return False
                        else: #use exact or underuse letters
                            decision = True #return True
                 
                    
          
                else: #if i used letters not in my hand
                    return False
                
                
            else: #if my word doesn't exist in wordlist
                vowels_count += 0
 
                
        if vowels_count != 0 and decision == True: #if it has at least one match and i didn't overuse
            return True
        
        else:
            return False
          
    else: #if my word doesn't contain * #1#
        word_testing = word_lower   
        if word_testing in word_list: #if my word exists in wordlist
                for i in range(len(my_word)):
                    if  my_word[i] in my_hand:
                        in_hand = True  
                    else:
                        in_hand = False
                 
                if in_hand == True:
                    for key in word_dic:
                        hand_num = new_hand.get(key, 0)
                        word_num = word_dic[key]
                        if word_num > hand_num:
                            return False
                        else:
                            return True
          
                else:
                    return False
        else:
            return False
        
# word = 'j*b'
# hand = {'j': 1, 'w': 1, '*': 1, 'l': 1, 'b': 2, 'o': 1, 'e': 2} #expected true
# word_list = load_words()
# print (is_valid_word(word, hand, word_list))

#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    handlen = 0
    for key in hand:
        handlen += hand.get(key, 0)
    return handlen


# hand = {'n': 1, 'h': 1, '*': 1, 'y': 1, 'd': 1, 'w': 1, 'e': 2} #expected true
# word_list = load_words()
# print (calculate_handlen(hand))


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    
    # Keep track of the total score
    total_score = 0
    # n = input("How many letters of a hand would you like to start with?")
    # hand = deal_hand(n)
    
    
    
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:
        # Display the hand
        print("Current hand:", display_hand(hand))
        # Ask user for input
        word = input ("Enter word, or !! to indicate that you are finished: ")
        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list) == True:
                # Tell the user how many points the word earned,
                score = get_word_score(word, n)
                total_score += score
                print (word, "earned", score, "points. Total:", total_score, "points")
                # and the updated total score

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print ("This is not a valid word. Please choose another word.")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),

    # so tell user the total score
    print ("Total score: ", total_score)
    print ("--------------------------")
    # Return the total score as result of function
    return total_score

# n = 10
# hand = deal_hand(n)
# word_list = load_words()
# play_hand(hand, word_list)


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    

    sub_hand = hand.copy()
    # letter = input("Which letter would you like to replace: ")

    my_hand = []

    
    for i in hand:
        my_hand.append(i) #create a list of letters in my hand
    
    if letter in my_hand:
                
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        generate = ''
        for i in alpha:
            if i != letter:
                generate += i
      
        x = random.choice(generate)
        
        sub_hand[x] = sub_hand.pop(letter)
        return sub_hand
    
    else:
        return sub_hand
       
# hand = {'a': 1, 'p': 2, 'l': 1, 'e': 1}
# letter = 'p'  
# print (substitute_hand(hand, letter))
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    hand_number = int(input("Enter total number of hands: "))

    total_score = 0
    
    play_again = ''
    
    while hand_number != 0 and play_again != 'no': #if enough hand number and i wanna play
        hand_number -= 1  #decrease hand number
        
        hand = deal_hand(n) #generate a hand
        print("Current hand:", display_hand(hand)) #display hand
        
        #substitute a letter
        sub_boolean = input("Would you like to substite a letter? (yes/no) ") 
        if sub_boolean == 'yes': #i wanna sub letter
            letter = input("Which letter would you like to replace: ")
            hand = substitute_hand(hand, letter)
            # print("Current hand:", display_hand(hand)) #display hand
        else:
            pass
            # print("Current hand:", display_hand(hand)) #display hand
        
        total_score += int(play_hand(hand, word_list))
        # play_hand(hand, word_list) #play hand      
        
        if hand_number != 0:
            play_again = input("Would you like to replay the hand? (yes/no) ")
            
        else:
            break
        
        # total_score += int(play_hand(hand, word_list))
        
        
    print("End of the game.")
    print("Your overall score is",total_score)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
