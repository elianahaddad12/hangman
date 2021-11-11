#################################################################
# FILE : hangman.py
# WRITER : Eliana Haddad , elianahaddad , 336378450
# EXERCISE : intro2cs1 ex4 2021
# DESCRIPTION: hangman game
# STUDENTS I DISCUSSED THE EXERCISE WITH: Hadas Grossztein, hadas2000
# WEB PAGES I USED:
# NOTE :
#################################################################
import hangman_helper


def update_word_pattern(word: str, pattern: str, letter):
    """
    this function receives a word, the pattern, and the letter that was guessed
    and changes the pattern to match the word (adds the given letter if exists)
    :param word: the full word - string
    :param pattern: the pattern that has been guess until now, with _ for
    unknown characters - string
    :param letter: the given letter - string
    :return: the new pattern - string
    """

    pattern = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            pattern[i] = letter

    return ''.join(pattern)


def guess_letter(letter, word, pattern, score, wrong_guessed_lst,
                 right_guessed_lst):
    """
    check if player entered a valid guess and if right update pattern
    :param letter: guessed character
    :param word: right word
    :param pattern: the pattern
    :param score: the user score
    :param wrong_guessed_lst: wrong guesses
    :param right_guessed_lst: right guesses
    :return: updated score, pattern, guessing lists and print parameter
    """

    # if the input is not one lower case letter
    if len(letter) > 1 or not letter.isalpha() or letter.isupper():
        print_parameter = "The letter you entered is " + '\033[91m' + \
                          "invalid." + '\033[0m'
    else:

        # if the input was already guessed in the past
        if letter in wrong_guessed_lst or letter in right_guessed_lst:
            print_parameter = "The letter you entered was already " \
                              "chosen "
        else:
            score = score - 1
            count = word.count(letter)
            if count:
                pattern = update_word_pattern(word, pattern, letter)
                score = score + (count * (count + 1)) // 2
                right_guessed_lst.append(letter)
            else:
                wrong_guessed_lst.append(letter)
            print_parameter = ""
    return score, pattern, wrong_guessed_lst, right_guessed_lst, \
        print_parameter


def guess_word(guessed_word, word, pattern, score):
    """
    if player guessed a word
    :param guessed_word: player input
    :param word: the right word
    :param pattern: the pattern
    :param score: user score
    :return: updated score and pattern
    """

    score -= 1
    if guessed_word == word:
        count = pattern.count("_")
        score = score + (count * (count + 1)) // 2
        pattern = word
    return score, pattern


def asked_hint(words_list, pattern, wrong_guessed_lst):
    """
    if player asked for a hint
    :param words_list: all word options
    :param pattern: updated pattern
    :param wrong_guessed_lst: wrong guesses
    :return: none
    """

    hints = filter_words_list(words_list, pattern, wrong_guessed_lst)
    number_of_hints = len(hints)
    new_hint_list = []
    if number_of_hints > hangman_helper.HINT_LENGTH:
        for i in range(hangman_helper.HINT_LENGTH):
            new_hint_list.append(
                hints[(i * number_of_hints) // hangman_helper.HINT_LENGTH])
    else:
        new_hint_list = hints
    hangman_helper.show_suggestions(new_hint_list)
    return


def end_game(score, word, pattern):
    """
    if game ended print the correct string
    :param score: user score
    :param word: right word
    :param pattern: updated pattern
    :return: string with print parameter
    """

    print_parameter = ""
    # if player has 0 points - user lost
    if not score:
        print_parameter = "You lost the game. The word was: " + word
    # if no "_" in pattern - user guessed the word and won
    elif "_" not in pattern:
        print_parameter = "You won the game!"
    return print_parameter


def run_single_game(words_list, score):
    """
    this function runs one single game
    :param words_list: list of wrong guessed words
    :param score: the points the player has
    :return: updated score of player
    """

    word = hangman_helper.get_random_word(words_list)
    pattern = "_" * len(word)
    wrong_guessed_lst = []
    right_guessed_lst = []
    print_parameter = ""
    while score != 0 and "_" in pattern:
        hangman_helper.display_state(pattern, wrong_guessed_lst, score,
                                     print_parameter)
        player_input = hangman_helper.get_input()
        # if the player guessed a letter
        if player_input[0] == hangman_helper.LETTER:
            score, pattern, wrong_guessed_lst, right_guessed_lst, \
                print_parameter = guess_letter(player_input[1], word, pattern,
                                               score, wrong_guessed_lst,
                                               right_guessed_lst)
        # if the player guessed a word
        elif player_input[0] == hangman_helper.WORD:
            score, pattern = guess_word(player_input[1], word, pattern, score)
        # if the player asked for a hint
        elif player_input[0] == hangman_helper.HINT:
            score -= 1
            asked_hint(words_list, pattern, wrong_guessed_lst)
    # checking if game ended
    if not print_parameter:
        print_parameter = end_game(score, word, pattern)
    hangman_helper.display_state(pattern, wrong_guessed_lst, score,
                                 print_parameter)
    return score


def main():
    """
    main function
    :return: none
    """

    word_list = hangman_helper.load_words()
    score = hangman_helper.POINTS_INITIAL
    play = True
    game = 0
    while play:
        game = game + 1
        score = run_single_game(word_list, score)
        # if the player won and still has points
        if score:
            msg = "Number of games so far: " + str(game) + \
                  ". Your current score: " + str(score) + ". Want to continue?"
        # if the player lost with no points left
        else:
            msg = "Number of games survived: " + str(game) + \
                  ". Start a new series of game? "
            score = hangman_helper.POINTS_INITIAL
            game = 0
        play = hangman_helper.play_again(msg)


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    this func filters the words that fits the pattern and previous guesses
    :param words: a list of words
    :param pattern: the pattern
    :param wrong_guess_lst: a list of wrong guesses
    :return: list of words from the words list that fit the pattern and
    previous guesses
    """

    option_lst = []
    # checking word by word in list
    for word in words:
        letters = 0
        if len(word) == len(pattern):
            # checking if letter match the pattern and wrong guesses
            for letter, char in zip(word, pattern):
                if letter == char or (char == "_" and letter not in
                                      wrong_guess_lst):
                    # checking if the letter appears more times in the word
                    # than in the pattern - if it does, the word can't be right
                    if word.count(letter) > pattern.count(letter) > 0:
                        break
                    letters = letters + 1
            # if all letters in word match the pattern add it to hints list
            if letters == len(word):
                option_lst.append(word)
    return option_lst


if __name__ == "__main__":
    main()
