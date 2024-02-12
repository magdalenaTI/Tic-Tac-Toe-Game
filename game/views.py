from django.shortcuts import render, HttpResponse, redirect
from game.models import Room
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == "GET" :
        return render(request, "index.html")
    elif request.method == "POST":
        print(request.POST)
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
    return render(request, "game.html")