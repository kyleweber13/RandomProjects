import PySimpleGUI as gui
import DiceGame
import random
import numpy as np

dice_nums = [1, 2, 3, 4, 5, 6]


def roll_dice(n_dice):

    new_roll = []

    for die in range(n_dice):
        new_roll.append(random.choice(dice_nums))

    return new_roll


def enter_name_window():

    layout = [[gui.Text("Player 1's name"), gui.InputText("Player #1")],
                [gui.Text("Player 2's name"), gui.InputText("Player #2")],
                [gui.Button('Ok')]]

    # Create the Window
    window = gui.Window('Enter player names', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    event, names = window.read()

    print("\nWelcome, {} and {}.".format(names[0], names[1]))
    print("\nLet the game begin!")

    window.close()

    p1 = DiceGame.Player(name=names[0])
    p2 = DiceGame.Player(name=names[1], other_player=p1)
    p1.other_player = p2

    return p1, p2


def score_roll(input_dice, total_score, actual_output=True):

    continue_turn = True

    new_points = 0

    used_dice = []
    remaining_dice = input_dice.copy()

    # Count for how many of each dice value were rolled
    # I.e. zero 1's, one two...
    die_count = [remaining_dice.count(i) for i in range(1, 7)]

    # Yahtzee ----------------------------------------------------------------------------------------------------
    if 5 in die_count:
        print("YAHTZEE, BITCHES. You win!")
        quit()

    # Four of a Kind ---------------------------------------------------------------------------------------------
    if 4 in die_count:

        # Determines which dice value is the four-of-a-kind
        which_four = die_count.index(4) + 1

        # Assigns points
        if which_four == 1:
            new_points = 2000
            used_dice = [1, 1, 1, 1]
        if which_four == 2:
            new_points = 400
            used_dice = [2, 2, 2, 2]
        if which_four == 3:
            new_points = 600
            used_dice = [3, 3, 3, 3]
        if which_four == 4:
            new_points = 800
            used_dice = [4, 4, 4, 4]
        if which_four == 5:
            new_points = 1000
            used_dice = [5, 5, 5, 5]
        if which_four == 6:
            new_points = 1200
            used_dice = [6, 6, 6, 6]

    # Full House and Three Ones ----------------------------------------------------------------------------------
    if 3 in die_count and 2 in die_count:

        # Checks to see if there ones were rolled --> worth more than full house
        # Determines which dice value is the three-of-a-kind
        which_three = die_count.index(3) + 1

        # If three-of-a-kind was with ones, assigns 1000 points
        if which_three == 1:
            new_points = 1000
            used_dice = [1, 1, 1]

        # If three-of-a-kind was not with ones, assigns 750 for full house
        if which_three != 1:
            new_points = 750
            remaining_dice = []

    # Straight ---------------------------------------------------------------------------------------------------
    if [1, 2, 3, 4, 5] == sorted(remaining_dice) \
            or [2, 3, 4, 5, 6] == sorted(remaining_dice) \
            and len(remaining_dice) == 5:
        new_points = 750
        remaining_dice = []

    # Three-of-a-kinds -------------------------------------------------------------------------------------------

    if remaining_dice.count(1) == 3:
        new_points = 1000
        used_dice = [1, 1, 1]
    if remaining_dice.count(2) == 3:
        new_points = 200
        used_dice = [2, 2, 2]
    if remaining_dice.count(3) == 3:
        new_points = 300
        used_dice = [3, 3, 3]
    if remaining_dice.count(4) == 3:
        new_points = 400
        used_dice = [4, 4, 4]
    if remaining_dice.count(5) == 3:
        new_points = 500
        used_dice = [5, 5, 5]
    if remaining_dice.count(6) == 3:
        new_points = 600
        used_dice = [6, 6, 6]

    if len(remaining_dice) != 0:
        for used_die in used_dice:
            remaining_dice.remove(used_die)

    # Couting remaining 1's and 5's -------------------------------------------------------------------------------
    new_points += 100 * remaining_dice.count(1)
    new_points += 50 * remaining_dice.count(5)

    if 5 in remaining_dice:
        remaining_dice.remove(5)
    if 1 in remaining_dice:
        remaining_dice.remove(1)

    # Output -----------------------------------------------------------------------------------------------------
    if actual_output:
        if new_points == 0:
            print("\n" + "Turn over!")
            continue_turn = False

        if total_score + new_points > 10000:
            print("\nBUSTED! Too many points...")
            continue_turn = False

        return new_points, continue_turn

    if not actual_output:
        return new_points


def roll_window(name, total_score, already_held_dice):

    n_dice = 5 - len(already_held_dice) % 5

    # New dice that were rolled
    dice = roll_dice(n_dice=n_dice)

    # List of checkboxes for each new die rolled
    checkboxes = [gui.Text('Dice to hold', font=("Helvetica", 15))]

    for die in range(len(dice)):
        checkboxes.append(gui.Checkbox(dice[die], font=("Helvetica", 15)))

    # Window layout
    layout = [

        # Line 1: displays player's score
        [gui.Text("Score: {} / 10000".format(total_score), font=("Helvetica", 15))],

        # Line 2: displays dice already being held as a textbox
        [gui.Text("Already held dice  ", font=("Helvetica", 15)),
         gui.InputText(already_held_dice, font=("Helvetica", 15))],

        # Line 3: displays dice that were rolled as a textbox
        [gui.Text("You rolled:", font=("Helvetica", 15)), gui.InputText(dice, font=("Helvetica", 15))],

        # Line 4: checkboxes for which dice to hold
        checkboxes,

        # Line 5: buttons to hold (continue turn) or end turn
        [gui.Button("Roll Again", button_color=('white', 'green'), enable_events=True, key='Roll Again'),
        gui.Button("End Turn", button_color=('black', 'red'), enable_events=False, key='End Turn')]]

    # Creates window. Title includes player's name
    window = gui.Window("{}'s turn".format(name), layout).finalize()

    # Reads in data from the window
    # Data values: 0 = already held dice, 1 = rolled dice, 2 through 6 = checkbox value for holding each rolled die
    event, data = window.read()

    # Boolean values from dice hold checkboxes
    dice_hold_values = [i for i in data.values()]

    # ACTIONS ----------------------------------------------------------------------------------------------------

    # If no dice are held
    if True not in dice_hold_values:
        print("No new dice held. End of turn.")
        new_holds = []
        roll_again = False

    # If dice are held
    if True in dice_hold_values:
        potential_holds = [int(die) for die_num, die in enumerate(data[1]) if
                           die != "(" and die != "," and die != " " and die != ")"]

        new_holds = [die for ind, die in enumerate(potential_holds) if data[ind+2]]

        print("New holds:", new_holds)

    if len(new_holds) > 0:
        for new_die in new_holds:
            already_held_dice.append(new_die)

    print("Holding: ", already_held_dice)

    if event == "Roll Again":
        roll_again = True
    if event == "End Turn":
        roll_again = False

    window.close()

    # Resets n_dice_left to 5 if all dice are scoring
    n_dice_left = 5 - len(already_held_dice) % 5

    score_roll(input_dice=new_holds, total_score=total_score, actual_output=False)

    return already_held_dice, n_dice_left, 0, roll_again

# player1, player2 = enter_name_window()
# continue_turn, new_holds, data, n_dice_left = roll_window(name="Kyle", total_score=5000, already_held_dice=[1, 1])
