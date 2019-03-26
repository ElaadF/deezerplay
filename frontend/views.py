from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from frontend.Word2Vec import all_list,pred_list

# Create your views here.

def library(request):
    context = {"navbar" : "library", "library": all_list()}
    print(all_list())
    return render(request, "frontend/index.html", context)

def playlist(request):
    context = {"navbar" : "playlist"}
    print(all_list())
    return render(request, "frontend/playlist.html", context)

def research(request):
    context = {"navbar" : "research"}
    return render(request, "frontend/research.html", context)

def researchParameters(request):
    context = {"navbar" : "research"}
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    try:
        track = request.GET['track']
        artist = request.GET['artist']
        return render(request, "frontend/research.html", context)
    except :
        messages.error(request, "Le groupe n'existe pas")
        return redirect('/research')


# def get_url_image(artist, track, lastfm_key):
#     params = {
#         "include" : "minimal",
#         "method" :  "track.getInfo",
#         "api_key" : lastfm_key,
#         "artist" : artist,
#         "track" : track,
#         "format" : "json",
#     }
#
#     json_data_accepted = requests.get("http://ws.audioscrobbler.com/2.0", params = params, verify = False)
#     json_nodes_accepted = json.loads(json_data_accepted.text)
#
#     accepted_nodes = {}
#     pending_nodes = {}
#
#     for node in json_nodes_accepted["data"]["nodes"]:
#         accepted_nodes[node["hostname"]] = node["id"]
#
#     return {"urls" : accepted_nodes, "pending_nodes": pending_nodes}
