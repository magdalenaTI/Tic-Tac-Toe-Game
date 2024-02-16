from django.shortcuts import render, HttpResponse, redirect
from game.models import *
from django.contrib import messages

from django.shortcuts import render
from django.http import JsonResponse
import sys

emptyCell = ''
maxScore = 10
minScore = -10
isPersonTurn = False
computerSymbol = ''
personSymbol = ''
invalidPosition = -1

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        roomId = request.POST.get("room-id", None)
        playerName = request.POST.get("player-name", "Unknown")
        if(roomId):
            try:
                room = Room.objects.get(id=roomId)
                return redirect(f"/game/{room.id}/{playerName}/")
            except Room.DoesNotExist:
                messages.error(request, "Room does not exist")
                return redirect("/")
        else:
            room = Room.objects.create()
            return redirect(f"/game/{room.id}/{playerName}/")


def game(request, id=None, name=None):
    try:
        room = Room.objects.get(id=id)
        return render(request, "game.html", {"room": room, "name": name})
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist")
        return redirect("/")
    
#####
def gameAI(request):

    if request.method == 'GET':
        return render(request, 'AI_game.html')
    
board = {
    0: '', 1: '', 2: '',
    3: '', 4: '', 5: '',
    6: '', 7: '', 8: '',
}

def evaluateBoard(depth):
    # Checking rows for victory
    for row in range(3):
        if board[row*3] == board[row*3 + 1] == board[row*3 + 2]:
            if board[row*3] == computerSymbol:
                return maxScore - depth
            elif board[row*3] == personSymbol:
                return minScore + depth

    # Checking columns for victory 
    for col in range(3):
        if board[col] == board[col + 3] == board[col + 6]:
            if board[col] == computerSymbol:
                return maxScore - depth
            elif board[col] == personSymbol:
                return minScore + depth

    # Checking main diagonal for victory 
    if board[0] == board[4] == board[8]:
        if board[0] == computerSymbol:
            return maxScore - depth
        elif board[0] == personSymbol:
            return minScore + depth

    # Checking second diagonal for victory
    if board[2] == board[4] == board[6]:
        if board[2] == computerSymbol:
            return maxScore - depth
        elif board[2] == personSymbol:
            return minScore + depth

    #If it is tied => return 0
    return 0


def areThereMovesLeft():
    for cell in board.values():
        if cell == emptyCell:
            return True
    return False

def maximizer(a, b, depth):
    curScore = evaluateBoard(depth)
    
    #Check if some of the players is winning
    if curScore != 0:
        return curScore
    
    #No moves left and no winner
    if not areThereMovesLeft():
        return 0
    
    #Initialize best score for max player is the smallest possible number
    bestScore = -sys.maxsize - 1

    for i in range(9):
        if board[i] == emptyCell:
            board[i] = computerSymbol

            #Recursive call, maximizer
            bestScore = max(bestScore, minimizer(a, b, depth + 1))

            #Undo so maximizer can try next possible moves
            board[i] = emptyCell

            if bestScore >= b:
                return bestScore
            a = max(a, bestScore)
    return bestScore

def minimizer(a, b, depth):
    curScore = evaluateBoard(depth)
    
    #Check if some of the players is winning
    if curScore != 0:
        return curScore
    
    #No moves left and no winner => tied
    if not areThereMovesLeft():
        return 0
    
    # nitialize best score for min player is the biggest possible number
    bestScore = sys.maxsize

    for i in range(9):
        if board[i] == emptyCell:
            board[i] = personSymbol

            #Recursive call, minimizer
            bestScore = min(bestScore, maximizer(a, b, depth + 1))

            #Undo so minimizer can try next possible moves
            board[i] = emptyCell

            if bestScore <= a:
                return bestScore
            b = min(b, bestScore)
    return bestScore

def findBestTurnForComputer():
    bestValue = -sys.maxsize - 1
    bestNextTurn = invalidPosition

    for i in range(9):
        if board[i] == emptyCell:
            board[i] = computerSymbol

            curTurnValue = minimizer(-sys.maxsize - 1, sys.maxsize, 0)

            # Undo 
            board[i] = emptyCell

            if curTurnValue > bestValue:
                bestNextTurn = i
                bestValue = curTurnValue
    return bestNextTurn

def isThereWinner():
    return evaluateBoard(0) != 0

def ai_move(request):
    if request.method == 'POST':
        game_state = request.POST.get('game_state')

        # Perform AI move using minimax algorithm
        ai_move = findBestTurnForComputer(game_state)

        # Send the updated game state as a JSON response
        return JsonResponse({'ai_move': ai_move})
    