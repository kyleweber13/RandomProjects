# KYLE WEBER HAD TIME TO KILL DURING THE GREAT CORONAVIRUS QUANARTINE OF MARCH 2020
import random
import time

"""
                                                        GAME RULES
                                                   
-Classic family game played with 2+ players and 5 dice

HOW A TURN WORKS

Player rolls 5 dice. Similar to Yatzhee, you may choose to hold dice. 

However, you may only hold dice that add to your score. You do not need to hold all your scoring dice.

You cannot add on to already held dice like you can in Yatzhee; scoring dice must be rolled in the same roll.

Scoring dice include:
        -Ones: 100 points per one
        -Fives: 50 points per five
        -Full house and straight: 750 points
        -Three-of-a-kind: three ones = 1000, three twos = 200, three threes = 300, 
                          three fours = 400, three fives = 500, three sixes = 600
        -Four-of-a-kind: double the respective three-of-a-point value
        -Yatzhee: automatic and devastating victory (1/1296; good luck)

Once you pick your dice to hold, you may roll the remaining dice. 
If you can add to your score, repeat above. You may choose to stop and take your points, or roll again.
    -There is no limit to the number of rolls, but your turn ends if you cannot add to your score. 
        -If you do not choose to end your turn and you roll a non-scoring roll, you get no points.
    -If all 5 of your dice are scoring, you may roll all 5 again and add on to your score.

Note: at the start of a game, you must score 500 points to "break the ice". You cannot take less than 500 points before
your ice is broken. 
Once your ice is broken, you will then be able to pile onto your opponents' turns (more on this later).

EXAMPLE OF A TURN
-You roll [1, 2, 1, 5, 6]

-There are no three/four-of-a-kinds, straights or full houses SO you count your 1s and 5s.
    -You could hold [1, 1, 5] or just [1, 1] or even just [1]
    
-If you hold onto just [1], you would roll the remaining 4 dice
-Let's say you roll [1, 1, 2, 3]
    -You would hold [1, 1]. You now have three ones, HOWEVER, only three/four-of-a-kinds/straights/full houses that
     were rolled in a single roll count.
        -For this round, you score 100 from the first 1, and then 200 for the next 2 ones. 
        -If your ice is broken, you may take these 300 points and end your turn.
    -If you hold onto [1, 1] and choose to roll again and roll [4, 6], you have no new scoring dice. 
     Your turn is over and you get no points.

PILING ONTO YOUR OPPONENTS' SCORE
-Once your ice is broken, if the opponent who goes before you scores points, you have the option to roll their 
 non-scoring dice to attempt to add on to their score. If you choose not to roll on their score, start again with 
 all 5 dice and 0 points.

-For example, if your opponent rolls [1, 1, 1, 1, 2] and takes their 2000 points (four ones = 2000 points), you may
 roll the remaining non-scoring die (the 2).
    -If you roll a scoring die (with 1 or 2 dice, rolling a 1 or 5 are the only options; with 3 dice, three-of-a-kind 
     is also an option), you add your roll on to the previous 2000 points. In this case, all 5 dice are scoring so 
     you can roll all 5 again for more points. 
    -If you do not roll a scoring di(c)e, your turn is over. The next player starts with 0 points and all 5 dice.
    
HOW TO WIN
-The first player to score exactly 10 000 points wins.
-If you are close to 10 000 points and your roll puts you over 10 000 points, your turn is over and you do not add
 to the score that you had at the start of your turn. 
 
 
                                                     PLAYING INSTRUCTIONS

SET UP
-You will be prompted to input both players' names in the console once you run the script.

PLAYING
-At the start of each player's turn, it will print their name and their current total score.
-The dice you rolled will be printed in the "Rolled dice: " line
-It will tell you how many potential points you can score this turn, and how many could be added on your current roll
 if you take the highest scoring option from the available dice

-You will be prompted to type in what dice to hold. For example, if you roll [1, 2, 5, 5, 6], you can type 115 to 
 hold both ones and the five. You do not need spaces or puncutation
    -If you try and hold dice you don't have, you will be asked to try again
    -If your dice don't add to your score, you will be asked to try again

-After you select your dice to hold, you will be asked to roll again with. Type y or n for your response.

-If you roll again, repeat the process. The first new line will let you know what dice are being held and the
 second line will show your new dice.
 -If you end your turn, your score will be added to your total score.
 -If you end your score with less than 500 points when your ice is not broken, it will automatically roll again.
 
-If you have broken your ice, and your opponent scored with dice left, you will be prompted as to whether you want to 
roll _ number of dice on top of _ number of points. 
"""


class Player:

    def __init__(self, name, other_player=None, cheat=False):

        self.dice_nums = [1, 2, 3, 4, 5, 6]

        if cheat:
            self.dice_nums = [random.choice(self.dice_nums)] * 6

        self.name = name
        self.other_player = other_player
        self.broken_ice = True
        self.total_score = 0
        self.scoring_round = False
        self.score_to_pass = 0
        self.dice_to_pass = []

    def play_a_turn(self):

        print("\n===============================================================================================")
        print("{}'s Turn ({} points)".format(self.name, self.total_score))
        print("===============================================================================================")

        time.sleep(2)

        continue_turn = True
        continue_previous_round = False
        roll_again = True
        n_dice = 5
        held_dice = []
        turn_score = 0
        self.scoring_round = False
        self.score_to_pass = 0
        self.dice_to_pass = []

        if self.broken_ice and len(self.other_player.dice_to_pass) >= 1:
            print()
            continue_previous_round = \
                input("Continue previous turn ({} "
                      "points and {} dice remaining): y/n?".format(self.other_player.score_to_pass,
                                                                   5 - len(self.other_player.dice_to_pass)))

            if continue_previous_round == "y" or continue_previous_round == "Yes" \
                    or continue_previous_round == "yes":
                held_dice = self.other_player.dice_to_pass
                n_dice = 5 - len(held_dice)
                turn_score = self.other_player.score_to_pass

        while continue_turn and roll_again:

            rolled, continue_turn = self.roll_dice(n_dice=n_dice, holding_dice=held_dice, input_score=turn_score)

            if continue_turn:
                held_dice, n_dice, roll_score, roll_again = self.hold_dice(holding_dice=held_dice,
                                                                           input_dice=rolled,
                                                                           prev_score=turn_score)

            if not continue_turn:
                break

            turn_score += roll_score

            if turn_score >= 500:
                self.broken_ice = True

            if self.broken_ice and not roll_again:
                self.scoring_round = True

                self.total_score += turn_score

                print("\n" + "Turn score: {}".format(turn_score))
                print("Total score: {}".format(self.total_score))

    def roll_dice(self, n_dice, holding_dice, input_score=0):

        print("\n" + "-----------------------------------------------------------------------------------------------")
        continue_turn = True

        if continue_turn and n_dice == 0:
            n_dice = 5

        new_roll = []

        for die in range(n_dice):
            new_roll.append(random.choice(self.dice_nums))

        print("Holding dice: {}".format(holding_dice))
        print("Rolled dice: {}".format(new_roll))

        new_points, continue_turn = self.score_roll(input_dice=new_roll)

        possible_score = input_score

        if continue_turn:
            possible_score += new_points
            print("{} potential points this turn (added {} with this roll).".format(possible_score, new_points))
        if not continue_turn and possible_score > 0:
            if self.broken_ice:
                print("No points for you. Coulda had {} points, you greedy S.O.B.".format(possible_score))
            if not self.broken_ice:
                print("No points for you.")
        if not continue_turn and possible_score == 0:
            print("No points for you.")

        return new_roll, continue_turn

    def score_roll(self, input_dice, actual_output=True):

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

        # Ones not here; included in full house scoring

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

            if self.total_score + new_points > 10000:
                print("\nBUSTED! Too many points...")
                continue_turn = False

            return new_points, continue_turn

        if not actual_output:
            return new_points

    def hold_dice(self, holding_dice, input_dice, prev_score):

        valid_hold = False
        reprint_input_dice = False

        # Loops until dice being held are legit, man
        while not valid_hold:

            # Reprints rolled dice upon subsequent loops
            if reprint_input_dice:
                print("Rolled dice: {}".format(input_dice))

            # Dice being held:user input
            dice = input("\n" + "Dice to hold: ")

            # Holds all dice if user inputs 'all'
            if dice == "all":
                dice = input_dice

            # List of newly-held dice, removes commas and spaces
            new_dice = [int(i) for i in dice if i != "," and i != " "]

            # All dice being held
            all_dice = [int(i) for i in holding_dice] + new_dice

            # Die count for both input dice and held dice
            rolled_count = [input_dice.count(i) for i in range(1, 7)]
            held_count = [new_dice.count(i) for i in range(1, 7)]

            # Determines if any held dice is not an input dice
            valid_hold_list = []
            for r, h in zip(rolled_count, held_count):
                valid_hold_list.append(h > r)

            # If player selected a die they didn't roll
            if True in valid_hold_list:
                print("Invalid dice selection. Try again. \n")
                valid_hold = False

            # If player only selected dice that they rolled
            if not True in valid_hold_list:
                valid_hold = True

                # If player only selected they rolled BUT those dice don't score any points
                if self.score_roll(input_dice=new_dice, actual_output=False) == 0:
                    print("Invalid dice selection; these dice don't score any points. Try again. \n")
                    valid_hold = False

            if not valid_hold:
                reprint_input_dice = True

        # If dice as held, prints which dice are held
        if len(dice) != 0:
            print("Holding onto", all_dice)

        # Calculates score of the roll/turn
        turn_score, continue_turn = self.score_roll(input_dice=new_dice)

        # Adds new score to previous score. Used in turn looping.
        prev_score += turn_score

        if self.total_score + prev_score == 10000:
            print("\n============================== We have a winner!!! ============================== ")
            print("Congratulations, {}!".format(self.name))
            print("Sucks to be you, {}...".format(self.other_player.name))
            print("\nFinal score")
            print("-{}: 10 000 points".format(self.name))
            print("-{}: {} points".format(self.other_player.name, self.other_player.total_score))
            quit()

        # Calculates how many dice are left to roll
        n_dice_left = 5 - (len(all_dice) % 5)

        # Resets n_dice_left to 5 if all dice are scoring
        if len(all_dice) % 5 == 0 and len(all_dice) != 0:
            n_dice_left = 5

        # Prompts user if they want to roll again
        roll_again = input("\n" + "Roll again with {} dice: y/n? ".format(n_dice_left))

        # Will continue with another turn if inputs "y", "yes" or "Y"
        if roll_again == "y" or roll_again == "yes" or roll_again == "Y":
            roll_again = True

        # What to do is player ends their turn
        if roll_again == "n" or roll_again == "no" or roll_again == "N":

            # Automatically rolls again if ice has not been broken and 500 points not attained
            if not self.broken_ice and prev_score < 500:
                print("\n" + "Ice not yet broken. I'll roll for you so you don't seem as dumb!")
                time.sleep(1)
                roll_again = True

            # Breaks ice and ends turn if ≥ points scored
            if not self.broken_ice and turn_score >= 500:
                print("\nIce has been broken!")
                self.broken_ice = True
                roll_again = False

            # Prints what dice are held at end of turn
            if self.broken_ice:
                print("\n" + "Final scoring dice: {}".format(all_dice))
                roll_again = False

            # Dice left in play which can be passed on to next player
            self.dice_to_pass = all_dice[-(5 - n_dice_left):]

            # Score that can get passed on to next player
            self.score_to_pass = prev_score

            # Prints dice and score that can be passed on to next player
            if self.other_player.broken_ice:
                print("Dice to pass on: ", self.dice_to_pass)
                print("Score to pass on: ", prev_score)

        return all_dice, n_dice_left, turn_score, roll_again


p1 = Player(name=input("Player 1's name: "))
p2 = Player(name=input("Player 2's name: "), other_player=p1)
p1.other_player = p2

while p1.total_score <= 10000 and p2.total_score <= 10000:
    p1.play_a_turn()
    time.sleep(1)
    p2.play_a_turn()
