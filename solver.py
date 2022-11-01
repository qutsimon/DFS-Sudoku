#do depth-first search
import numpy
import math


puzzle = [[9,0,0,1,7,0,4,0,2],
        [1,6,0,0,4,0,0,9,5],
        [0,0,8,0,0,3,0,0,0],
        [0,1,0,9,0,0,5,7,3],
        [0,4,0,0,0,0,0,2,0],
        [5,8,9,0,0,7,0,1,0],
        [0,0,0,4,0,0,7,0,0],
        [6,7,0,0,2,0,0,5,8],
        [3,0,1,0,5,8,0,0,6]] 

""" puzzle = [[1,5,0,0,9,2,0,0,0],
        [0,7,0,0,0,0,0,0,6],
        [0,0,0,5,7,8,0,0,0],
        [0,1,0,0,0,0,7,3,0],
        [0,0,0,0,0,5,0,0,0],
        [0,0,3,0,0,0,0,4,1],
        [0,0,0,0,0,0,0,0,0],
        [0,6,0,4,0,0,0,0,3],
        [3,0,4,7,5,9,6,0,0]]
 """


#assumes numpy array
#Returns list of available moves for each tile
#Returns a one-dimensional array of size row*col of puzzle
def get_tile_moves(puzzle, row, col):

    #make the moves list - stored in  one-dimesional array where index number 
    #coresponds to tile
    moves = [ [0] for i in range(row*col)]

    for i in range(0,row):
        for j in range(0, col):
            num = puzzle[i][j]
            temp = [num]
            #check to see if the number if already set, only check tiles that are already set
            if num == 0:
                #create list to remove moves that are already taken from
                temp = list(range(1, 10))
                temp_not_moves = []

                #Check row
                for value in puzzle[i]:
                    if value != 0:
                        if value not in temp_not_moves:
                            temp_not_moves.append(value)
                            temp.remove(value)
                #check col
                for row_num in range(0,9):
                    if puzzle[row_num][j] != 0:
                        if puzzle[row_num][j] not in temp_not_moves:
                            temp_not_moves.append(puzzle[row_num][j])
                            temp.remove(puzzle[row_num][j])


                #check sub-grid
                #gives top left element of the grid that we are in
                square_edge = int(math.sqrt(row))
                grid_row = i//square_edge * square_edge
                grid_col = j//square_edge * square_edge

                for sub_row in range(0,3):
                    for sub_col in range(0,3):
                        if puzzle[grid_row+sub_row][grid_col+sub_col] != 0:
                            if puzzle[grid_row+sub_row][grid_col+sub_col] not in temp_not_moves:
                                temp_not_moves.append(puzzle[grid_row+sub_row][grid_col+sub_col])
                                temp.remove(puzzle[grid_row+sub_row][grid_col+sub_col])                            

                moves[i*row+j] = temp

            #if number is set add that number only to that tiles moves
            else: 
                moves[i*row+j] = temp
 
    return moves

#checks if a number is valid for a specific tile
#Returns true if valid, false  otherwise
def tile_valid_move(puzzle, move, row, col):
    valid = True
    
    #row check
    if move in puzzle[row] and puzzle[row][col] != move:
        valid = False

    #col check
    for row_num in range(0,9):
        if move == puzzle[row_num][col] and puzzle[row][col] != move:
            valid = False
    
    #sub-grid check
    square_edge = int(math.sqrt(puzzle.shape[0]))
    grid_row = row//square_edge * square_edge
    grid_col = col//square_edge * square_edge
    for sub_row in range(0,3):
        for sub_col in range(0,3):
            if puzzle[grid_row+sub_row][grid_col+sub_col] == move and puzzle[row][col] != move:
                valid = False

    return valid

#Fills in the puzzle array with moves that are already decided
#Where Moves_list[index] length == 0
def fill_in_only(puzzle, move_list):
    index = 0
    for moves in move_list:
        if len(moves) == 1:
            row_num = index // 9
            col_num = index % 9
            puzzle[row_num][col_num]= moves[0]
        index += 1

#Solve the puzzle
def solve():
    #change puzzle array to numpy_arr so that we can get size
    puzzle_arr = numpy.asarray(puzzle)
    #should be a square but who knows
    row_size = puzzle_arr.shape[0]
    col_size = puzzle_arr.shape[1]

    print("Inital Puzzle")
    print(puzzle_arr)
    print("\n")
    moves = get_tile_moves(puzzle_arr, row_size, col_size)

    #hardcoded range - just for now
    move_nums = [ 0 for i in range(row_size*col_size)]

    fill_in_only(puzzle_arr,moves)
    
    current = 0
    while current < row_size*col_size:
        row_num = current // row_size
        col_num = current % col_size
        ##check if it moved backwards and if there is only one element - index out of range
        if move_nums[current] == 1 and len(moves[current]) == 1:
            move_nums[current] = 0
            move_nums[current-1] += 1
            current -= 1
            print("Only one Move. Moving back a step")
        #for moving backwards alot
        elif move_nums[current] >= len(moves[current]):
            puzzle_arr[row_num][col_num] = 0
            move_nums[current-1] += 1
            move_nums[current] = 0
            current -= 1
            print("Ran out of moves. Moving back a step")
        elif tile_valid_move(puzzle_arr,moves[current][move_nums[current]],row_num, col_num):
            puzzle_arr[row_num][col_num] = moves[current][move_nums[current]]
            print("Placed " + str(moves[current][move_nums[current]]) + " in location: " +
                str(row_num) + "," + str(col_num))
            current += 1
        #if not valid try next move - if no moves move backward and try different move
        else:
            if move_nums[current] >= len(moves[current])-1:
                puzzle_arr[row_num][col_num] = 0
                move_nums[current-1] += 1
                move_nums[current] = 0
                current -= 1
                print("Ran out of moves. Moving back a step")
            else:
                #if another move, try it first
                move_nums[current] += 1
                    
    print("\nFinished")
    print(puzzle_arr)


def main():
    #program description

    #Wait for input to start
    input("Press Enter key to start...\n")

    #Start program
    solve()

if __name__ == "__main__":
    main()