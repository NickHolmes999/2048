from tkinter import *
from tkinter import messagebox
import random


class GameBoard:
    bg_color = {
        '2': '#eee4da',
        '4': '#ede0c8',
        '8': '#edc850',
        '16': '#edc53f',
        '32': '#f67c5f',
        '64': '#f65e3b',
        '128': '#edcf72',
        '256': '#edcc61',
        '512': '#f2b179',
        '1024': '#f59563',
        '2048': '#edc22e',
    }
    color = {
        '2': '#776e65',
        '4': '#f9f6f2',
        '8': '#f9f6f2',
        '16': '#f9f6f2',
        '32': '#f9f6f2',
        '64': '#f9f6f2',
        '128': '#f9f6f2',
        '256': '#f9f6f2',
        '512': '#776e65',
        '1024': '#f9f6f2',
        '2048': '#f9f6f2',
    }

    def __init__(self):
        self.n = 4
        self.window = Tk()
        self.window.title('2048')
        self.gameArea = Frame(self.window, bg='azure3')
        self.board = []
        self.gridCell = [[0] * 4 for i in range(4)]
        self.compress = False
        self.merge = False
        self.moved = False
        self.score = 0

        for i in range(4):
            rows = []
            for j in range(4):
                label = Label(self.gameArea, text='', bg='azure4', font=('arial', 22, 'bold'), width=4, height=2)
                label.grid(row=i, column=j, padx=7, pady=7)
                rows.append(label)
            self.board.append(rows)

        self.gameArea.grid()

    def reverse_rows(self):
        for row in self.gridCell:
            row.reverse()

    def transpose_grid(self):
        self.gridCell = [list(t) for t in zip(*self.gridCell)]

    def compress_grid(self):
        self.compress = False
        temp = [[0] * 4 for _ in range(4)]
        for i in range(4):
            k = 0
            for j in range(4):
                if self.gridCell[i][j] != 0:
                    temp[i][k] = self.gridCell[i][j]
                    if j != k:
                        self.compress = True
                    k += 1
        self.gridCell = temp
        self.add_random_cell()

    def merge_grid(self):
        self.merge = False
        for i in range(4):
            for j in range(4 - 1):
                if self.gridCell[i][j] == self.gridCell[i][j + 1] and self.gridCell[i][j] != 0:
                    self.gridCell[i][j] *= 2
                    self.gridCell[i][j + 1] = 0
                    self.score += self.gridCell[i][j]
                    self.merge = True

    def add_random_cell(self):
        empty_cells = []
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    empty_cells.append((i, j))
        if len(empty_cells) > 0:
            row, col = random.choice(empty_cells)
            existing_numbers = [2, 2, 4]
            matching_numbers = [num for num in existing_numbers if
                                num in [self.gridCell[i][j] for i in range(4) for j in range(4)]]
            if matching_numbers:
                self.gridCell[row][col] = random.choice(matching_numbers)
            else:
                self.gridCell[row][col] = random.choice(existing_numbers)

    def can_merge_cells(self):
        for i in range(4):
            for j in range(3):
                if self.gridCell[i][j] == self.gridCell[i][j + 1]:
                    return True

        for i in range(3):
            for j in range(4):
                if self.gridCell[i + 1][j] == self.gridCell[i][j]:
                    return True

        return False

    def paint_grid(self):
        for i in range(4):
            for j in range(4):
                if self.gridCell[i][j] == 0:
                    self.board[i][j].config(text='', bg='azure4')
                else:
                    self.board[i][j].config(text=str(self.gridCell[i][j]),
                                            bg=self.bg_color.get(str(self.gridCell[i][j])),
                                            fg=self.color.get(str(self.gridCell[i][j])))
class GameManager:
    def __init__(self, game_board):
        self.game_board = game_board
        self.end = False
        self.won = False

    def start_game(self):
        self.game_board.add_random_cell()
        self.game_board.add_random_cell()
        self.game_board.paint_grid()
        self.game_board.window.bind('<Key>', self.link_keys)
        self.game_board.window.mainloop()

    def link_keys(self, event):
        if self.end or self.won:
            return
        self.game_board.compress = False
        self.game_board.merge = False
        self.game_board.moved = False
        pressed_key = event.keysym
        if pressed_key == 'Up':
            self.game_board.transpose_grid()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.moved = self.game_board.compress or self.game_board.merge
            self.game_board.compress_grid()
            self.game_board.transpose_grid()
        elif pressed_key == 'Down':
            self.game_board.transpose_grid()
            self.game_board.reverse_rows()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.moved = self.game_board.compress or self.game_board.merge
            self.game_board.compress_grid()
            self.game_board.reverse_rows()
            self.game_board.transpose_grid()
        elif pressed_key == 'Left':
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.moved = self.game_board.compress or self.game_board.merge
            self.game_board.compress_grid()
        elif pressed_key == 'Right':
            self.game_board.reverse_rows()
            self.game_board.compress_grid()
            self.game_board.merge_grid()
            self.game_board.moved = self.game_board.compress or self.game_board.merge
            self.game_board.compress_grid()
            self.game_board.reverse_rows()
        else:
            pass
        self.game_board.paint_grid()
        print(self.game_board.score)
        flag = 0
        for i in range(4):
            for j in range(4):
                if self.game_board.gridCell[i][j] == 2048:
                    flag = 1
                    break
        if flag == 1:
            self.won = True
            messagebox.showinfo('2048', message='You Won!!')
            print("won")
            return
        for i in range(4):
            for j in range(4):
                if self.game_board.gridCell[i][j] == 0:
                    return
        self.end = True
        messagebox.showinfo('2048', message='Game Over')

game_board = GameBoard()
game_manager = GameManager(game_board)
game_manager.start_game()
