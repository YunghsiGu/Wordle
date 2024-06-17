import random
from os import system

GREEN = '\x1b[48;5;28m'
YELLOW = '\x1b[48;5;100m'
GRAY = '\x1b[48;5;240m'
RED = '\x1b[91;22m'
PURPLE = '\x1b[95;22m'
RESET = '\x1b[0m'

played_times = 0
win = 0
again = 'y'

def create_word_list(length):
    with open('.\words_alpha.txt', 'r', encoding='utf-8') as fd:
        word_list = list()
        words = fd.read().split()
        for i in range(len(words)):
            if len(words[i]) == length:
                word_list.append(words[i])
        return word_list

def no_such_length(word_list):
    if len(word_list) == 0:
        print(RED)
        print('No such word length\n', RESET)
        print('Press enter to continue...')
        input()
        return True

def chance_lower_than_one(chance):
    if chance < 1:
        print('')
        print('If you don\'t wanna play, just press ctrl + C')
        print('Press enter to continue...')
        input()

def print_chance(chance):
    print(PURPLE)
    if chance == 1:
        print('%d' % chance, 'chance left')
    else:
        print('%d' % chance, 'chances left')             
    print(RESET)

def select_mode():
    y_or_n = input('Do you want to switch to hard mode? (y/n) ').lower()
    if y_or_n == 'y':
        return True
    else:
        return False

def random_answer(word_list):
    index = random.randrange(len(word_list))
    answer = str(word_list[index])
    print(PURPLE)
    print('Answer:', answer)
    return answer

"""
hard_mode:  You have to put the letter at the correct position
            if knowing. Also, use the letter if you know the 
            word contains it.
"""
def hard_mode(index_record, letter_record, answer, guess):
    i = 0
    for j in guess:
        # Check whether the place is recorded; compare the answer with the input.
        if i in index_record and answer[i] != j:
            print(RED)
            print('Index', i + 1, 'has to be', answer[i], RESET)
            return 'fail'
        i += 1

    for i in letter_record:
        if not i in guess:
            print(RED)
            print('You have to input letter', i, RESET)
            return 'fail'

"""
statistics: Show the summary of performance.
"""
def statistics(played_times, win):
    print('\n=== STATISTICS ===\n')
    print('%d' % played_times, 'played')
    print('%d' % win, 'win')
    print('%d' % (played_times - win), 'lose')
    print('%.f' % (100 * win / played_times), '% win')
    print('')

def play_again(played_times, win):
    y_or_n = input('Do you want to play again? (y/n): ').lower()
    if y_or_n == 'n':
        statistics(played_times, win)
    return y_or_n

random.seed()

while again == 'y': 
    played_times += 1
    
    # reset
    length_error = True
    index_record = list()
    letter_record = list()

    while length_error:
        system('cls')
        length = int(input('Input the word length you want: '))      
        word_list = create_word_list(length)

        if no_such_length(word_list):
            continue

        chance = int(input('Input the chances you want: '))
        if chance_lower_than_one(chance):
            continue

        in_hard_mode = select_mode()
        answer = random_answer(word_list)

        while chance > 0:
            print_chance(chance)         
            guess = input('Input your guess: ')

            # length error
            if len(guess) == length:
                length_error = False

                if guess in word_list:
                    chance -= 1
                    if in_hard_mode:
                        if hard_mode(index_record, letter_record, answer, guess) is 'fail':
                            chance += 1
                            continue
                    # judge
                    print('')
                    i = 0
                    for j in guess:
                        if answer[i] == j:
                            print(GREEN, j.upper(), end=' ')
                            index_record.append(i)
                        elif j in answer:
                            print(YELLOW, j.upper(), end=' ')
                            letter_record.append(j)
                        else:
                            print(GRAY, j.upper(), end=' ')
                        print(RESET, end=' ')
                        i += 1
                    print('')

                    if guess == answer:
                        print('\n=== CONGRATS! ===\n')
                        win += 1
                        break
                else:
                    print(RED)
                    print('Not in word list', RESET)
            else:
                print(RED)
                print('Length error', RESET)
        else:
            print('\n=== FAIL ===\n')
    again = play_again(played_times, win)
