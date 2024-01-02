import chess
import chess.pgn
import os


path = input('Enter the path of your database directory:\n') #Path toward the database containing PGN files
your_game = input('Enter the path of your game file:\n') #Path toward the PGN file of the game
for_opening = input('Up to how many opening moves should the games used by the programs have in common with your game ? :\n') 
for_sample = input('What is the minimum number of games that the program should use ? :\n') 
my_color = input('Black or White to move ?')
files = os.listdir(path) #List all files in the database


def mklist(game):  #Makes string list of all the half moves in a chess.pgn game
   
    global lmoves  #The list
    lmoves = [] 
    
    board = game.board()    #Creates a board
    
    for move in game.mainline_moves():  
        
        lmoves.append(board.san(move))  #Collect the moves into the list
        board.push(move)                #Makes a move on the board


def mklist_legal(game): #Makes string list of all the legal moves in the given position
    
    global legal         #The list
    legal = []
    
    board = game.board()  #Creates a board
    
    for move in game.mainline_moves():    #Plays the game on board
        board.push(move)
    
    a = board.legal_moves                 #Finds legal moves in the board where all the moves have been played
    
    for move in a:                        #Collect the moves into the list
        legal.append(board.san(move))



def compare_weak(l1, l2):    #Compares two lists of strings. Returns true if l2 contains l1. 
    if list(set(l1) & set(l2)) == list(set(l1)):
        return True
    else:
        return False
    

def compare_strong(l1, l2, n_open):    #Compares openings up to move number n_open and returns True if they have the same opening
    
    n1 = len(l1)                   #Finds the minimum between n_open and the length of either lists
    n2 = len(l2)
    n = min(n1,n2)
    n = min(n,n_open)
    
    if l1[0:n] == l2[0:n]:
        return True
    else:
        return False
    
def same_opening(game, n_open): #Finds all games in the database with the same opening up to move number n_open. 

    mklist(game)                  
    l_game = lmoves                     
    
    global same_open           #List containing all such games 
        
    same_open = []
    
    for file in files:         #Goes through every files in the database
        
        f = path+"/"+file
        pgn = open(f)
        
        y = True              #Bool to close a file the file and open the next after all the games in the file have been analysed
        
        while y == True:
            
            fg = chess.pgn.read_game(pgn)
            
            if fg != None:
                mklist(fg)
                l1 = lmoves

                x = compare_strong(l_game, l1, n_open)
                
                if x == True:
                    same_open.append(fg)     #Collects the game if it has the same opening as our input game
            else:                            #This means there are no more games in the file
                y = False
        pgn.close()

def best_move(game, n_open, n_data, color):
    
    if color == "White":                             #Condition to identify games with positive outcome
        goal = "1-0"
    elif color == "Black":
        goal = "0-1"
    else:
        return "The color needs to be White or Black."
    
    mklist_legal(game)                                
    
    if len(legal) == 0:                             #If there is no legal move, this means the game is finished
        return "The game is finished"
    
    if len(legal) == 1:                             #If there is only one legal move, no need to run anything else                         
        return legal
    
    same_opening(game, n_open)
    
    if len(same_open) < n_data:
        return "Not enough games with the same opening in the database."    
    
    prob = []            #List containing probability of victory for each legal move
    
    
    for lms in legal:   #Go through all legal moves
        
        p_games = 0     #Counts all the data games that have the same opening than our input game and that contain all the moves from the input game 
        p_win = 0       #Among those game, counts those where our color win   
        
        mklist(game)       #Add the loop's legal move to our input game
        l_game = lmoves
        l_game.append(lms)
        
        for g in same_open: #Go through all games with the same opening as our input game
                        
            mklist(g)                            
            x = compare_weak(l_game, lmoves)  
            
            if x == True:              #If all the moves in the input game are found in the data game
                p_games = p_games + 1
                
                if g.headers["Result"] == goal:  #If our color win 
                    p_win = p_win + 1
                    
        if p_games < n_data:  #If the number of games corresponding to our criteria is too low
            pro = 0
            
        else:
            pro = p_win / p_games #Probability of vitory for this legal move
        
        prob.append(pro)  
    
    best = max(prob)             #Find the move with the best probability
    b_index = prob.index(best)
    print(legal[b_index])



pgn =  open(your_game)
the_game = chess.pgn.read_game(pgn)

best_move(the_game, int(for_opening), int(for_sample), my_color)
