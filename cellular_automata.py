from backend import *
from matplotlib import pyplot as plt

def iterate(board):
    # Neighbors array to find 8 neighboring cells for a given cell
    neighbors = [(1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1), (1,1)]

    rows = len(board)
    cols = len(board[0])

    # Create a copy of the original board
    copy_board = [[board[row][col] for col in range(cols)] for row in range(rows)]

    # Iterate through board cell by cell.
    for row in range(rows):
        for col in range(cols):

            # For each cell count the number of live neighbors.
            live_neighbors = 0
            for neighbor in neighbors:

                r = (row + neighbor[0])
                c = (col + neighbor[1])

                # Check the validity of the neighboring cell and if it was originally a live cell.
                # The evaluation is done against the copy, since that is never updated.
                if (r < rows and r >= 0) and (c < cols and c >= 0) and (copy_board[r][c] == 1):
                    live_neighbors += 1

            # Rule 1 or Rule 3        
            if copy_board[row][col] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                board[row][col] = 0
            # Rule 4
            if copy_board[row][col] == 0 and live_neighbors == 3:
                board[row][col] = 1
    return board

if __name__ == '__main__':
    #create desired game
    new_game = PPAC(n_rows=20, n_cols=20, visuals_on=True)
    #new_game.print_board()
    new_game.iterate(100)
    print(new_game.saved_data, new_game.probabilities)
    #information is saved in created object, use saved_data to view data, create graphs and plots, etc...
    data = [(i.Generation, i.NumberOfPrey, i.NumberOfPredators) for i in new_game.saved_data]
    time_stamps = [i[0] for i in data]
    prey_pop = [i[1] for i in data]
    pred_pop = [i[2] for i in data]
    plt.figure()
    plt.plot(time_stamps, prey_pop)
    plt.legend("Prey")
    plt.plot(time_stamps, pred_pop)
    plt.legend("Predators")
    plt.show()



#Define the rules
#Create the board, with a certain amount of predator and prey cells/nodes
    #Iterate the board according to the rules
    #Save the board state(number of predators/prey) for each step
#After a certain amount of times/steps or when the board is empty, plot the population dynamics
#Plot the population dynamics according to Lotka-Volterra equations with initial board parameters
#/(number of prey, number of predators, chance to reproduce/be eaten
#Compare CA plots to LV plots,

