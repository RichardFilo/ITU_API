from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import *
import json
# Create your views here.
def games(request):
    if request.method == 'GET':
        items = Game.objects.filter(state='lobby')
        response = [{ 'id': item.id, 'player':item.player1 } for item in items]
        return JsonResponse({'rooms':response}, safe=False)

    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['name']
        print(content)
        game = Game(player1=content)
        game.save()
        return JsonResponse({"id":game.id, "player":game.player1},status=201)

def game(request, id):
    item = get_object_or_404(Game, id=id)

    if request.method == 'GET':
        response = { 'id': item.id, 'chessboard':item.chessboard, 'player1':item.player1, 'player2':item.player2, 'state': item.state, "onTurn": item.onTurn }
        return JsonResponse(response, safe=False)
    
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['name']
        print(content)
        item.player2 = content
        item.state = 'start'
        item.save()
        return JsonResponse({'id': item.id, 'chessboard':item.chessboard, 'player1':item.player1, 'player2':item.player2, 'state': item.state, "onTurn": item.onTurn},status=201)

    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse({"result":"deleted"})

def click(request, id):
    item = get_object_or_404(Game, id=id)

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        x = body['tah']
        if isValid(x):
            item.click(x)
        else:
            return JsonResponse({"response":"Not valid"})
        chessboard = returnString()
        print(x, chessboard)
        printBoard()
        return JsonResponse({"response":chessboard})


def finish(request, id):
    item = get_object_or_404(Game, id=id)

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        x = body['state']
        print(x) 
        if x == 0:
            item.state = "remiza"
        elif x == 1:
            item.state = "vyhral 1"
        elif x == 2:
            item.state = "vyhral 2"
        item.save()
        return JsonResponse({"state": item.state})
    