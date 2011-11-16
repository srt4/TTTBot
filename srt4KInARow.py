import copy
import math


def is_terminal(node):
    return staticEval(node[1]) is 1234567

def minimaxAB(node,A,B,turn, depthlimit = 0):
    if hashCode(node[1]) in hashMins:
       return hashMins[hashCode(node[1])] 
    am = allMoves(node[1])
    if is_terminal(node) or depthlimit < 1:
        hashMins[hashCode(node[1])] = (A, B, staticEval(node[1]))
        return staticEval(node[1])
    if turn is 'max':
        for child in am:
            A = max(A, minimaxAB(child, A, B, 'min', depthlimit - 1))
            if B <= A:
                break
        hashMins[hashCode(node[1])] = (A, B, A)
        return A
    else:  # 'min'
        for child in am:
            B = min(B, minimaxAB(child, A, B, 'max', depthlimit - 1))
            if B <= A: 
                break
        hashMins[hashCode(node[1])]  = (A, B, B)
        return B

def prepare(k0, initialState, maxMillisecPerMove, isPlayingX, debugging):
    global k
    k = k0
    global hashMins
    global hashEvals
    global movesHash
    movesHash = {}
    hashMins = {}
    hashEvals = {}
    if (len(initialState[0]) < k and len(initialState[0][0]) < k):
    	return "This is silly. We can't play on a board that's smaller than k!"
    return "OK"

def nickname():
    return "Denzel"

def introduce():
    return '''Hi, I'm Denzel. I'm a tic-tac-toe
 playing bot written by Spencer <srt4 at uw>'''
    
# Returns positive for advantage to player 1, neg to adv for p2
def staticEval(state):
    global k
    global statesExamined
    global all_rows
    statesExamined += 1
    if hashCode(state) in hashEvals:
		return hashEvals[hashCode(state)]
    board = state[0]
    all_rows = []
    score = 0
    
    # Analyze rows
    for row in board:
        all_rows.append(row)
        
    # Transpose
    sideways = zip(*board)
    # Add columns
    for column in sideways:
        all_rows.append(column)
        
    # Add diags
    for diag in diagRows(state):
        all_rows.append(diag)
    	
    # Analyze, row-by-row
    for row in all_rows:
    	rowScore = 0
    	sum = rowTotal(row, 1) - rowTotal(row, 2)
    	rowScore = sum ** sum
        if rowScore is 1:
    		rowScore = 0
    	score += rowScore
    	
    #for row in state[0]:
   	#	print str(row)
   	hashEvals[hashCode(state)] = score
    return score

def rowTotal(row, symbol):
	i = 0
	for column in row:
		if column is symbol:
			i = i+1
	return i

def hashCode(state):
    return hash(str(state))

def diagRows(state):
    global k
    # Alright... Broderick's AI likes to use diagonals
    #board = state[0]
    boards = (state[0], zip(*state[0]))
    rows = []
    for board in boards: 
		firstRow = board[0]
		rowLength = len(firstRow)
		colLength = len(board)
		for yIndex, thisRow in enumerate(board):
			for index,cell in enumerate(thisRow):
				x = index
				y = yIndex
				row = []
				while x < rowLength and y < colLength:
					row.append(board[y][x])
					x = x + 1
					y = y + 1
				if len(row) > k: # If this row can yield a win
					rows.append(row)
				x = index
				y = yIndex
				row = []
				while x >= 0 and y < colLength:
					row.append(board[y][x])
					x = x - 1
					y = y + 1
				if len(row) > k:
					rows.append(row)
    return rows

def bestMove(state):
    best_move = None
    #calculate all moves once
    am = allMoves(state)

    #for move in am:
    #    if best_move == None:
    #        best_move = move
    #    if staticEval(move[1]) > staticEval(best_move[1]):
    #        best_move = move
    moveScores = {}
    whoseMove = 'max'
    if state[1]:
        whoseMove = 'min'
    for move in am:
        moveScores[minimaxAB(move, -float('inf'), float('inf'), whoseMove)] = move
    if whoseMove is 'max':
        best_move = moveScores.get( min(moveScores.keys()) )
    else: 
        best_move = moveScores.get( max(moveScores.keys()) )
    return best_move

def makeMove(state, currentRemark, timeLimit = 10000):
    global statesExamined
    statesExamined = 0
    #call bestMove once!
    bm = bestMove(state)
    global all_rows
    return (bm[0], bm[1], wittyQuip(currentRemark, state), statesExamined)

def allMoves(state):
    'Returns a list in the format of [[move, newState], ...]'
    global movesHash
    if hashCode(state) in movesHash : 
    	return movesHash[hashCode(state)]
    newState = state
    board = newState[0]
    # if state[1]: 2, else 1
    movesList = []
    whoseMove = newState[1]
    for rowNum, row in enumerate(board):
        for colNum, square in enumerate(row):
            if square is 0:
                returnableBoard = copy.deepcopy(board)
                if not newState[1]: 
                    placement = 2
                else: 
                    placement = 1
                returnableBoard[rowNum][colNum] = placement
                movesList.append(((whoseMove, rowNum, colNum), (returnableBoard, not newState[1])))
    movesHash[hashCode(state)] = movesList
    return movesList


def wittyQuip(currentRemark, state):
	'Returns a witty quip- this bot gets overly confident when ahead, and overly unconfident when behind'
	
	remark = "I'm baffled"
	number = float(-staticEval(state))
	if number > 40:
		remark = "Better luck next time."
	elif number > 20:
		remark = "Yeah, I'm good."
	elif number > 10:
		remark = "Good luck winning this one."
	elif number > 0:
		remark = "I have a good feeling about this move."
	else: 
		if number < 60:
			remark = "Why do I even bother?"
		elif number < 40:
			remark = "Okay, fine! You win!"
		elif number < 20:
			remark = "Hmm, you're pretty good."
		elif number < 0:
			remark = "Grr... We'll see if this works."
	if "win" in currentRemark and number > 0:
		remark += " What makes you think you're going to win?"
	if "lose" in currentRemark and "you" in currentRemark:
		remark += " Don't count your eggs before they're hatched!"
	if " Ha " in currentRemark or "funny" in currentRemark:
		remark += " What's so funny?"
	return remark
	
