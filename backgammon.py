from random import randint
import sys

start_board = [["Z", "Y", "W", "V", "U", "T", "S", "R", "Q", "P", "N", "M"],
               ["X", " ", " ", " ", " ", "O", " ", "O", " ", " ", " ", "X"],
               ["X", " ", " ", " ", " ", "O", " ", "O", " ", " ", " ", "X"],
               [" ", " ", " ", " ", " ", "O", " ", "O", " ", " ", " ", "X"],
               [" ", " ", " ", " ", " ", "O", " ", " ", " ", " ", " ", "X"],
               [" ", " ", " ", " ", " ", "O", " ", " ", " ", " ", " ", "X"],
               [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
               [" ", " ", " ", " ", " ", "X", " ", " ", " ", " ", " ", "O"],
               [" ", " ", " ", " ", " ", "X", " ", " ", " ", " ", " ", "O"],
               [" ", " ", " ", " ", " ", "X", " ", "X", " ", " ", " ", "O"],
               ["O", " ", " ", " ", " ", "X", " ", "X", " ", " ", " ", "O"],
               ["O", " ", " ", " ", " ", "X", " ", "X", " ", " ", " ", "O"],
               ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]]

spaces_dict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
               "I": 9, "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "P": 15,
               "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22,
               "Y": 23, "Z": 24}
spaces_dict_bottom = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
                      "I": 8, "J": 9, "K": 10, "L": 11}
spaces_dict_top = {"Z": 0, "Y": 1, "W": 2, "V": 3, "U": 4, "T": 5, "S": 6,
                   "R": 7, "Q": 8, "P": 9, "N": 10, "M": 11}

class Board:
    def __init__(self, board):
        self.board = board
        self.jail = []

    def print_board(self):
        for row in self.board:
            row_str = ""
            for x in row:
                row_str += x
                row_str += " "
            print(row_str)
        if self.jail != []:
            print(" ")
            jail_str = ""
            for x in self.jail:
                jail_str += x
                jail_str += " "
            print("Jailed pieces: " + jail_str)
        if Player1.pieces_removed > 0:
            print(" ")
            player1_pieces_off_str = ""
            pieces_off = Player1.pieces_removed
            while pieces_off > 0:
                player1_pieces_off_str += "X"
                player1_pieces_off_str += " "
                pieces_off -= 1
            print("Player 1's Pieces Off: " + player1_pieces_off_str)
        if Player2.pieces_removed > 0:
            print(" ")
            player2_pieces_off_str = ""
            pieces_off = Player2.pieces_removed
            while pieces_off > 0:
                player2_pieces_off_str += "O"
                player2_pieces_off_str += " "
                pieces_off -= 1
            print("Player 2's Pieces Off: " + player2_pieces_off_str)

    def move_piece(self, current, destination, marker):
        #first, we find the piece to remove
        first_row = self.board[0]
        last_row = self.board[len(self.board) - 1]
        check_list = list(range(1, len(self.board) - 1))[::-1]
        jail_check = False
        if marker == "X":
            other_marker = "O"
        else:
            other_marker = "X"
        if current in first_row:
            for i in range(1, len(self.board)):
                if self.board[i][spaces_dict_top[current]] == marker and self.board[i + 1][spaces_dict_top[current]] == " ":
                    self.board[i][spaces_dict_top[current]] = " "
                    break
        elif current in last_row:
            for i in check_list:
                if self.board[i][spaces_dict_bottom[current]] == marker and self.board[i - 1][spaces_dict_bottom[current]] == " ":
                    self.board[i][spaces_dict_bottom[current]] = " "
                    break
        else: #implies piece is moving out of jail
            self.jail = remove_value(marker, self.jail)
        #next, we move this piece to the destination
        if destination in first_row:
            if self.board[1][spaces_dict_top[destination]] == other_marker:
                jail_check = True
                self.board[1][spaces_dict_top[destination]] = marker
            else:
                for i in range(1, len(self.board)):
                    if self.board[i][spaces_dict_top[destination]] == " ":
                        self.board[i][spaces_dict_top[destination]] = marker
                        break
        elif destination in last_row:
            if self.board[len(self.board) - 2][spaces_dict_bottom[destination]] == other_marker:
                jail_check = True
                self.board[len(self.board) - 2][spaces_dict_bottom[destination]] = marker
            else:
                for i in check_list:
                    if self.board[i][spaces_dict_bottom[destination]] == " ":
                        self.board[i][spaces_dict_bottom[destination]] = marker
                        break
        elif destination == "Off":
            if marker == "X":
                Player1.pieces_removed += 1
            else:
                Player2.pieces_removed += 1
        if jail_check == True:
            if other_marker == "X":
                self.jail.append("X")
                Player1.jailed_pieces +=1
            else:
                self.jail.append("O")
                Player2.jailed_pieces += 1
        #self.print_board()
        self.check_add_row()

    def remove_from_jail(self, rolls, available_spaces, marker):
        if marker == "X":
            if Player1.jailed_pieces == 1:
                print("You have 1 piece in jail. You must remove it before you can do anything else.")
            else:
                print("You have pieces in jail. You must remove them befoe you can do anything else.")
        else:
            if Player2.jailed_pieces == 1:
                print("You have 1 piece in jail. You must remove it befoe you can do anything else.")
            else:
                print("You have pieces in jail. You must remove them befoe you can do anything else.")
        print(" ")
        available_spaces_str = ""
        for x in available_spaces:
            available_spaces_str += x
            available_spaces_str += " "
        print("Available space(s) you can move to: " + available_spaces_str)
        print(" ")
        destination = input("Pick the available space you'd like to move your jailed piece to: ")
        if destination in available_spaces:
            board.move_piece("jail", destination, marker)
            if marker == "X":
                Player1.jailed_pieces -= 1
                distance = spaces_dict_top[destination] + 1
                rolls = remove_value(distance, rolls)
                Player1.take_turn(rolls)
            else:
                Player2.jailed_pieces -= 1
                distance = spaces_dict_bottom[destination] + 1
                rolls = remove_value(distance, rolls)
                Player2.take_turn(rolls)
        else:
            print(" ")
            print("Invalid input: Choice was not one of the available spaces. Try again.")
            self.remove_from_jail(rolls, available_spaces, marker)

    def check_add_row(self):
        threshold = len(self.board) - 2
        for col in range(0, 12):
            in_a_row = 0
            insert_space = 0
            for row in range(1, len(self.board) - 1):
                if self.board[row][col] == " ":
                    break
                else:
                    in_a_row += 1
                    if (self.board[row][col] == "X" and self.board[row + 1][col] == "O") or (self.board[row][col] == "O" and self.board[row + 1][col] == "X"):
                        insert_space = row
            if threshold == in_a_row:
                self.board.insert(insert_space + 1, [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "])
                break

    def check_current(self, current, marker):
        first_row = self.board[0]
        last_row = self.board[len(self.board) - 1]
        if current in first_row:
            if self.board[1][spaces_dict_top[current]] == marker:
                return True
            else:
                return False
        elif current in last_row:
            if self.board[len(self.board) - 2][spaces_dict_bottom[current]] == marker:
                return True
            else:
                return False
        else:
            return False

    def check_destination(self, destination, marker):
        first_row = self.board[0]
        last_row = self.board[len(self.board) - 1]
        if marker == "X":
            other_marker = "O"
        else:
            other_marker = "X"
        if destination in first_row:
            if self.board[1][spaces_dict_top[destination]] == marker or self.board[1][spaces_dict_top[destination]] == " ":
                return True
            elif self.board[1][spaces_dict_top[destination]] == other_marker and self.board[2][spaces_dict_top[destination]] == " ":
                return True
            else:
                return False
        elif destination in last_row:
            if self.board[len(self.board) - 2][spaces_dict_bottom[destination]] == marker or self.board[len(self.board) - 2][spaces_dict_bottom[destination]] == " ":
                return True
            elif self.board[len(self.board) - 2][spaces_dict_bottom[destination]] == other_marker and self.board[len(self.board) - 3][spaces_dict_bottom[destination]] == " ":
                return True
            else:
                return False
        elif destination == "Off":
            max_height = board.get_max_height(marker)
            if marker == "O":
                O_count = 0
                for col in range(0, 6):
                    for row in range(1, max_height + 1):
                        if self.board[row][col] == marker:
                            O_count += 1
                        else:
                            break
                if O_count == 15 - Player2.pieces_removed:
                    return True
                else:
                    return False
            else:
                reverse_list = list(range(max_height, len(self.board) - 1))[::-1]
                X_count = 0
                for col in range(0,6):
                    for row in reverse_list:
                        if self.board[row][col] == marker:
                            X_count += 1
                        else:
                            break
                if X_count == 15 - Player1.pieces_removed:
                    return True
                else:
                    return False
        else:
            return False

    def check_possible_moves(self, rolls, marker):
        if marker == "O":
            #check moves from top row first
            for col in range(0, 12):
                if self.board[1][col] == marker:
                    current_position_val = spaces_dict[get_key(spaces_dict_top, col)]
                    for roll in rolls:
                        possible_destination_val = current_position_val + roll
                        if possible_destination_val >= 1 and possible_destination_val <= 24:
                            possible_destination = get_key(spaces_dict, possible_destination_val)
                        else:
                            possible_destination = "Off"
                        if self.check_destination(possible_destination, marker):
                            return True
            #check moves from bottom row
            for col in range(0, 12):
                if self.board[len(self.board) - 2][col] == marker:
                     current_position_val = spaces_dict[get_key(spaces_dict_bottom, col)]
                     for roll in rolls:
                        possible_destination_val = current_position_val + roll
                        if possible_destination_val >= 1 and possible_destination_val <= 24:
                            possible_destination = get_key(spaces_dict, possible_destination_val)
                        else:
                            possible_destination = "Off"
                        if self.check_destination(possible_destination, marker):
                            return True
            return False
        else:
            #check moves from top row first
            for col in range(0, 12):
                if self.board[1][col] == marker:
                    current_position_val = spaces_dict[get_key(spaces_dict_top, col)]
                    for roll in rolls:
                        possible_destination_val = current_position_val - roll
                        if possible_destination_val >= 1 and possible_destination_val <= 24:
                            possible_destination = get_key(spaces_dict, possible_destination_val)
                        else:
                            possible_destination = "Off"
                        if self.check_destination(possible_destination, marker):
                            return True
            #check moves from bottom row
            for col in range(0, 12):
                if self.board[len(self.board) - 2][col] == marker:
                     current_position_val = spaces_dict[get_key(spaces_dict_bottom, col)]
                     for roll in rolls:
                        possible_destination_val = current_position_val - roll
                        if possible_destination_val >= 1 and possible_destination_val <= 24:
                            possible_destination = get_key(spaces_dict, possible_destination_val)
                        else:
                            possible_destination = "Off"
                        if self.check_destination(possible_destination, marker):
                            return True
            return False

    def get_max_height(self, marker):
        if marker == "O":
            max_height = 1
            for col in range(0,6):
                counter = 0
                for row in range(1, len(self.board) - 1):
                    if self.board[row][col] == marker:
                        counter += 1
                    else:
                        break
                if counter > max_height:
                    max_height = counter
        else:
            reverse_list = list(range(1, len(self.board) - 1))[::-1]
            max_height = len(self.board) - 2
            for col in range(0,6):
                counter = len(self.board) - 1
                for row in reverse_list:
                    if self.board[row][col] == marker:
                        counter -= 1
                    else:
                        break
                if counter < max_height:
                    max_height = counter
        return max_height

class Player:
    def __init__(self, number, other_player, marker):
        self.number = number
        self.other_player = other_player
        self.marker = marker
        self.pieces_removed = 0
        self.jailed_pieces = 0

    def roll(self):
        dummy_input = input("Player {0}, press enter to roll: ".format(self.number))
        roll1, roll2 = randint(1,6), randint(1,6)
        print("Player " + str(self.number) + " has rolled a " + str(roll1) + " and a " + str(roll2))
        if roll1 == roll2:
            print("You've rolled doubles! You get double the amount of moves.")
            self.take_turn([roll1, roll1, roll1, roll1])
        self.take_turn([roll1, roll2])

    def take_turn(self, rolls):
        if self.pieces_removed == 15:
            self.win()
        if rolls != [] and self.jailed_pieces == 0 and not board.check_possible_moves(rolls, self.marker):
            print(" ")
            print("You have no possible moves! That means it's Player {0}'s turn.".format(self.other_player))
            self.next_turn()
        if rolls != []:
            print(" ")
            print("Here is the board:")
            board.print_board()
        if rolls!= [] and self.jailed_pieces == 0:
            print(" ")
            current = input("Pick the space of a piece you'd like to move: ")
            print(" ")
            if not board.check_current(current, self.marker):
                print("Invalid input. Try again.")
                self.take_turn(rolls)
            destination = input("Where would you like to move this piece to? ")
            print(" ")
            if not board.check_destination(destination, self.marker):
                print("Invalid destination. Please re-enter your inputs.")
                self.take_turn(rolls)
            if destination != "Off":
                non_abs_distance = spaces_dict[destination] - spaces_dict[current]
            else: #implies trying to move off board
                if self.number == 1:
                    non_abs_distance = 0 - spaces_dict[current]
                else:
                    non_abs_distance = 25 - spaces_dict[current]
            if (self.number == 1 and non_abs_distance >=0) or (self.number == 2 and non_abs_distance <=0):
                if non_abs_distance == 0:
                    print("You can't keep a piece in the same place. Please re-enter your inputs.")
                else:
                    print("Wrong direction! Try again.")
                self.take_turn(rolls)
            distance = abs(non_abs_distance)
            if destination != "Off":
                if distance in rolls:
                    board.move_piece(current, destination, self.marker)
                    if len(rolls) >= 2:
                        print("Next move: ")
                    rolls = remove_value(distance, rolls)
                    self.take_turn(rolls)
                else:
                    print("You can't move a piece that distance. Try again.")
                    self.take_turn(rolls)
            else: #implies trying to move off board
                if distance in rolls:
                    board.move_piece(current, destination, self.marker)
                    if len(rolls) >= 2 and self.pieces_removed != 15:
                        print("Next move: ")
                    rolls = remove_value(distance, rolls)
                    self.take_turn(rolls)
                else:
                    """Implies distance is not in rolls but that piece may be moved off board
                    if the distance is less than the rolls and there is no other available move."""
                    for roll in rolls:
                        if roll < distance:
                            print("You can't move a piece that distance. Try again.")
                            self.take_turn(rolls)
                    board.move_piece(current, destination, self.marker)
                    if len(rolls) >= 2 and self.pieces_removed != 15:
                        print("Next move: ")
                    rolls = remove_value(max(rolls), rolls)
                    self.take_turn(rolls)
        elif rolls != [] and self.jailed_pieces > 0:
            available_spaces = self.try_out_of_jail(rolls)
            if available_spaces != []:
                board.remove_from_jail(rolls, available_spaces, self.marker)
            else:
                print("You have no possible moves! That means it's Player {0}'s turn.".format(self.other_player))
                self.next_turn()
        else:
            print("Turn complete! Now it's Player {0}'s turn.".format(self.other_player))
            self.next_turn()

    def next_turn(self):
        if self.other_player == 2:
            Player2.roll()
        else:
            Player1.roll()

    def try_out_of_jail(self, rolls):
        if self.marker == "X":
            other_marker = "O"
        else:
            other_marker = "X"
        available_spaces = []
        if self.number == 1:
            for i in range(0, 6):
                if i + 1 in rolls and (board.board[1][i] == " " or board.board[1][i] == self.marker):
                    available_spaces += get_key(spaces_dict_top, i)
                elif i + 1 in rolls and (board.board[1][i] == other_marker and board.board[2][i] == " "):
                    available_spaces += get_key(spaces_dict_top, i)
        else:
            for i in range(0,6):
                if i + 1 in rolls and (board.board[len(board.board) - 2][i] == " " or board.board[len(board.board) - 2][i] == self.marker):
                    available_spaces += get_key(spaces_dict_bottom, i)
                elif i + 1 in rolls and (board.board[len(board.board) - 2][i] == other_marker and board.board[len(board.board) - 3][i] == " "):
                    available_spaces += get_key(spaces_dict_bottom, i)
        return available_spaces

    def win(self):
        print("Congratulations Player {0}, you win!".format(self.number))
        print("Thanks for playing backgammon! :)")
        sys.exit(" ")

Player1 = Player(1, 2, "X")
Player2 = Player(2, 1, "O")
board = Board(start_board)

def welcome_function():
    print(" ")
    print("Hi, welcome to backgammon!")
    print(" ")
    print("Player 1's pieces will be represented by X's.")
    print("Player 2's pieces will be represented by O's.")
    print(" ")
    print("On each turn, select the labeled space of the piece you want to move, and where you want to move it to.")
    print(" ")
    print("At the end of the game, if you want to move a piece off the board, type 'Off'.")
    print(" ")
    print("Each player will roll 1 die to start the game.")
    start_roller()

def start_roller():
    print(" ")
    dummy_input = input("Player 1, press enter to roll: ")
    roll1 = randint(1,6)
    print("Player 1 rolls a " + str(roll1))
    print(" ")
    dummy_input2 = input("Player 2, press enter to roll: ")
    roll2 = randint(1,6)
    print("Player 2 rolls a " + str(roll2))
    print(" ")
    if roll1 == roll2:
        print("Player 1 and Player 2 rolled the same number. Roll again!")
        start_roller()
    elif roll1 > roll2:
        choosing_player = 1
    else:
        choosing_player = 2
    print("Player {0} rolled a higher number, so player {1} goes first.".format(choosing_player, choosing_player))
    print(" ")
    print("Here is the starting board:")
    board.print_board()
    print(" ")
    print("Player {0}, would you like to keep this roll for your first move, or roll again?".format(choosing_player))
    choice = input("Type 'keep' to keep this roll, or 'roll' to roll again: ")
    if choosing_player == 1:
        if choice == "keep":
            Player1.take_turn([roll1, roll2])
        else:
            Player1.roll()
    else:
        if choice == "keep":
            Player2.take_turn([roll1, roll2])
        else:
            Player2.roll()

def remove_value(value, lst):
    if len(lst) == 1:
        return []
    elif lst[0] == value:
        return lst[1:]
    else:
        return [lst[0]] + remove_value(value, lst[1:])

def get_key(dictionary, val):
    for key, value in dictionary.items():
        if val == value:
            return key

welcome_function()
