# Author: Dave Huston
# Date: 14 August 2020
# Description: Portfolio Project black box game

class BlackBoxGame:
    """creates a class that represents the Black Box game"""

    def __init__(self, atoms):
        """initializes board and current state and takes places atoms on the board"""

        row1 = ["", "", "", "", "", "", "", "", "", ""]
        row2 = ["", "", "", "", "", "", "", "", "", ""]
        row3 = ["", "", "", "", "", "", "", "", "", ""]
        row4 = ["", "", "", "", "", "", "", "", "", ""]
        row5 = ["", "", "", "", "", "", "", "", "", ""]
        row6 = ["", "", "", "", "", "", "", "", "", ""]
        row7 = ["", "", "", "", "", "", "", "", "", ""]
        row8 = ["", "", "", "", "", "", "", "", "", ""]
        row9 = ["", "", "", "", "", "", "", "", "", ""]
        row10 = ["", "", "", "", "", "", "", "", "", ""]

        board = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]
        self._board = board
        self._score = 25
        self._atoms_left = len(atoms)
        self._tracker = []
        self._ray = [0, 0]

        if self.valid_atom(atoms):
            for item in atoms:
                atom_row = item[0]
                atom_col = item[1]
                board[atom_row][atom_col] = "o"

    def shoot_ray(self, shot_row, shot_col):
        """takes a coordinate for the ray to be shot from and returns tuple value of exit location or None if atoms is hit. Else return false"""

        if self.valid_shot(shot_row, shot_col):
            return True
        self.add_to_tracker(shot_row, shot_col)
        self._ray = self.shot_direction(shot_row, shot_col)

        #check if initial move is a reflection
        if self.check_reflection(shot_row, shot_col):
            return (shot_row, shot_col)

        #check if location in front of ray contains an atom
        if self._board[shot_row + self._ray[0]][shot_col + self._ray[1]] == 'o':
            return None

        shot_row += self._ray[0]
        shot_col += self._ray[1]
        while 0 < shot_row < 9 and 0 < shot_col < 9:
            if self._board[shot_row + self._ray[0]][shot_col + self._ray[1]] == 'o':
                return None
            self.check_deflection(shot_row, shot_col)
            self.check_double_deflection(shot_row, shot_col)
            shot_row += self._ray[0]
            shot_col += self._ray[1]

        self.add_to_tracker(shot_row, shot_col)
        return (shot_row, shot_col)

    def valid_atom(self, atoms):
        """check to see if atoms are being places in valid spot and return true else return false"""
        for item in atoms:
            atom_row = item[0]
            atom_col = item[1]
            if atom_row == 0 or atom_row == 9 or atom_col == 0 or atom_col == 9:
                return False
            else:
                return True

    def valid_shot(self, shot_row, shot_col):
        """check to see if shot is valid and return true if it is, else return false"""
        shot = (shot_row, shot_col)
        if shot == (0, 0) or shot == (0, 9) or shot == (9, 0) or shot == (9, 9):
            return True
        elif shot_row in range(1, 9) and shot_col == 0 or shot_col == 9:
            return False
        elif shot_col in range(1, 9) and shot_row == 0 or shot_row == 9:
            return False

    def add_to_tracker(self, shot_row, shot_col):
        """checks if location has been tracked and adds to tracker and updates score if not"""
        shot = (shot_row, shot_col)
        if shot not in self._tracker:
            self._tracker.append(shot)
            self._score -= 1

    def shot_direction(self, shot_row, shot_col):
        """checks directions shot is fired and return direction"""
        direction = [0, 0]
        #if ray is moving rows
        if shot_row == 0:
            direction[0] = 1
        if shot_row == 9:
            direction[0] = -1
        #if ray is moving columns
        if shot_col == 0:
            direction[1] = 1
        if shot_col == 9:
            direction[1] = -1
        return direction

    def check_reflection(self, shot_row, shot_col):
        """check to see if a shot has been reflected and returns true if so, else return false"""
        #if ray is moving rows
        if self._ray[0] != 0 and self._board[shot_row + self._ray[0]][shot_col-1] == 'o':
            return True
        if self._ray[0] != 0 and self._board[shot_row + self._ray[0]][shot_col+1] == 'o':
            return True
        #if ray is moving columns
        if self._ray[1] != 0 and self._board[shot_row - 1][shot_col + self._ray[1]] == 'o':
            return True
        if self._ray[1] != 0 and self._board[shot_row + 1][shot_col + self._ray[1]] == 'o':
            return True

    def check_deflection(self, shot_row, shot_col):
        """check to see if the shot has been deflected and return new direction"""
        #if ray is moving rows
        if self._ray[0] != 0 and self._board[shot_row + self._ray[0]][shot_col-1] == 'o':
            self._ray = [0, 1]
        if self._ray[0] != 0 and self._board[shot_row + self._ray[0]][shot_col+1] == 'o':
            self._ray = [0, -1]
        #if ray is moving columns
        if self._ray[1] != 0 and self._board[shot_row - 1][shot_col + self._ray[1]] == 'o':
            self._ray = [1, 0]
        if self._ray[1] != 0 and self._board[shot_row + 1][shot_col + self._ray[1]] == 'o':
            self._ray = [-1, 0]

    def check_double_deflection(self, shot_row, shot_col):
        """check to see if the shot has been double deflected and return new direction"""
        #if ray is moving rows
        if self._ray[0] != 0 and self._board[shot_row + self._ray[0]][shot_col-1] == 'o' and self._board[shot_row + self._ray[0]][shot_col+1] == 'o':
            self._ray[0] = self._ray[0] * -1
            self._ray[1] = self._ray[1] * -1
        #if ray is moving columns
        if self._ray[1] != 0 and self._board[shot_row - 1][shot_col + self._ray[1]] == 'o' and self._board[shot_row + 1][shot_col + self._ray[1]] == 'o':
            self._ray[0] = self._ray[0] * -1
            self._ray[1] = self._ray[1] * -1

    def guess_atom(self, guess_row, guess_col):
        """guesses the coordinates of an atom, returns true is hit and subtracts an atom from, else returns false and updates score"""
        if self._board[guess_row][guess_col] == "o":
            #right guess subtracts an atom
            self._atoms_left -= 1
            return True
        else:
            #wrong guess subtracts from score
            self._score -= 5
            return False

    def get_score(self):
        """returns the score of the guessing player"""
        return self._score

    def atoms_left(self):
        """returns the number of atoms that have not yet been guessed"""
        return self._atoms_left

    def print_board(self):
        """print current board"""
        for row in self._board:
            print(row)

    def get_tracker(self):
        """returns tracker"""
        return self._tracker


game = BlackBoxGame([(3,2),(1,7),(4,6),(8,8)])
game.print_board()
move_result = game.shoot_ray(3,9)
game.shoot_ray(0,2)
guess_result = game.guess_atom(5,5)
score = game.get_score()
atoms = game.atoms_left()