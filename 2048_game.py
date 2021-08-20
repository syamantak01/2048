import tkinter as tk
import formatter as ft
import random

class game(tk.Frame):
    def __init__(self):
        super(game, self).__init__()
        self.grid()
        self.master.title('2048')

        self.main_grid = tk.Frame(self, bg = ft.GRID_COLOR, bd = 3, width = 400, height = 400) 
        self.main_grid.grid(pady = (100, 0))

        #make the board
        self.make_GUI()

        #start the game
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()
    
    def make_GUI(self): 
        #make game board
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(self.main_grid, bg = ft.EMPTY_CELL_COLOR, width = 100, height = 100)
                cell_frame.grid(row = i, column = j, padx = 5, pady = 5)
                cell_number = tk.Label(self.main_grid, bg = ft.EMPTY_CELL_COLOR)
                cell_number.grid(row = i, column = j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        #Make score card
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y = 45, anchor = "center")
        score = tk.Label(score_frame, text = "Score", font = ft.SCORE_LABEL_FONT)
        score.grid(row = 0)
        self.score_label = tk.Label(score_frame, text = "0", font = ft.SCORE_FONT)
        self.score_label.grid(row = 1)

    def start_game(self): 
        #create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        #fill 2 random cells with 2's
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg = ft.TILE_COLORS[2])
        self.cells[row][col]["number"].configure(bg = ft.TILE_COLORS[2], fg = ft.NUMBER_COLORS[2], font = ft.NUMBER_FONTS[2], text = "2")

        while (self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)

        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg = ft.TILE_COLORS[2])
        self.cells[row][col]["number"].configure(bg = ft.TILE_COLORS[2], fg = ft.NUMBER_COLORS[2], font = ft.NUMBER_FONTS[2], text = "2")

        #initialize the score with 0
        self.score = 0

    #To stack two cells
    def stack(self): 
        new_matrix = [[0] * 4 for _ in range(4)]

        for i in range(4):
            fill_position = 0   #fill_position keeps a track of the cells containing non zero numbers
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    #To combine two cells with same number and generating a single cell with that (number*2)
    def merge(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    self.matrix[i][j] = self.matrix[i][j] * 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]

    #reverse the order of each row in the matrix
    def reverse(self): 
        new_matrix = [[] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix = new_matrix

    #flip the matrix along its diagonal
    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    #randomly add a new 2 numbered cell/tile or 4 numbered cell 
    def add_cell(self):
        if any(0 in row for row in self.matrix):
            new_num = random.choice([2, 4])
            
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while self.matrix[row][col] != 0:
                row = random.randint(0, 3)
                col = random.randint(0, 3)

            self.matrix[row][col] = new_num

    #update the board to match the matrix   
    def update_board(self):
        for i in range(4):
            for j in range(4):
                #the value of the cell or the tile
                num = self.matrix[i][j]
                if num == 0:
                    self.cells[i][j]["frame"].configure(bg = ft.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg = ft.EMPTY_CELL_COLOR, text = "")
                else:
                    self.cells[i][j]["frame"].configure(bg = ft.TILE_COLORS[num])
                    self.cells[i][j]["number"].configure(bg = ft.TILE_COLORS[num], fg = ft.NUMBER_COLORS[num], font = ft.NUMBER_FONTS[num], text = str(num))

        self.score_label.configure(text = self.score)
        self.update_idletasks   #to immediately update the widget displays

    #Arrow-Press Functions

    def left(self, event): 
        self.stack()
        self.merge() 
        self.stack()
        self.add_cell()
        self.update_board()
        self.game_over()

    #right swipe is basically the left swipe on  reversed board and we reverse back again to have the originial board
    def right(self, event):
        self.reverse()
        self.stack()
        self.merge() 
        self.stack()
        self.reverse()
        self.add_cell()
        self.update_board()
        self.game_over()

    #up swipe is basically the left swipe on a transposed matrix/ board
    def up(self, event):
        self.transpose()
        self.stack()
        self.merge() 
        self.stack()
        self.transpose()
        self.add_cell()
        self.update_board()
        self.game_over()

    #In a similar manner, down swipe is basically the right swipe on a trasnposed matrix/board
    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.merge() 
        self.stack()
        self.reverse()
        self.transpose()
        self.add_cell()
        self.update_board()
        self.game_over()

    #to check if any move in the horizontal is possible
    def is_horizontal_possible(self):
        for i in range(4):
            for j in range(3): 
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return True
        return False

    #to check if any move in the vertical is possible
    def is_vertical_possible(self):
        for i in range(3):
            for j in range(4): 
                if self.matrix[i][j] == self.matrix[i+1][j]:
                    return True
        return False



    #Check if the game is finished (Win/Lose)
    def game_over(self): 
        if any(2048 in row for row in self.matrix):
            finish_frame = tk.Frame(self.main_grid, borderwidth = 2)
            finish_frame.place(relx = 0.5, rely = 0.5, anchor = "center")
            finish_msg = tk.Label(finish_frame, text = "Congratulation, you win", bg = ft.WINNER_BG, fg = ft.GAME_OVER_FONT_COLOR, font = ft.GAME_OVER_FONT)
            finish_msg.pack()
        elif not any(0 in row for row in self.matrix) and not self.is_horizontal_possible() and not self.is_vertical_possible():
            finish_frame = tk.Frame(self.main_grid, borderwidth = 2)
            finish_frame.place(relx = 0.5, rely = 0.5, anchor = "center")
            finish_msg = tk.Label(finish_frame, text = "Game Over!", bg = ft.LOSER_BG, fg = ft.GAME_OVER_FONT_COLOR, font = ft.GAME_OVER_FONT)
            finish_msg.pack()

#creates an instance of the game class
def main():
    game()

if __name__ == '__main__':
    main()
