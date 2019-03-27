from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from frontend.Word2Vec import all_list,pred_list, track_dict, trj_meta


def library(request):
    context = {"navbar": "library", "track": all_list(), "artist": all_list()}
    return render(request, "frontend/index.html", context)


def library_by_filter(request):
    lst = all_list();
    track_lst = list()
    artist_lst = list()
    letter = request.GET['letter']
    if letter is None:
        context = {"navbar": "library", "track": all_list(), "artist": all_list()}
        return render(request, "frontend/index.html", context)
    if letter == "digit":
        for dic in lst:
            if dic['title'][0].isdigit():
                track_lst.append(dic)
            if dic['name'][0].isdigit():
                artist_lst.append(dic)
        context = {"navbar": "library", "track": track_lst, "artist": artist_lst}
        return render(request, "frontend/index.html", context)
    for dic in lst:
        if dic['title'][0].upper() == letter:
            track_lst.append(dic)
        if dic['name'][0].upper() == letter:
            artist_lst.append(dic)
    context = {"navbar": "library", "track": track_lst, "artist": artist_lst}
    return render(request, "frontend/index.html", context)


def library_recommandation(request):
    reco_lst = list()
    id = request.GET['id']
    if id is None:
        context = {"navbar": "library", "track": reco_lst, "artist": reco_lst}
        return render(request, "frontend/index.html", context)
    id_lst = list()
    id_lst.append(track_dict[id])
    reco_lst = pred_list(id_lst)
    context = {"navbar": "library", "track": reco_lst, "artist": reco_lst}
    return render(request, "frontend/index.html", context)


def playlist(request):
    context = {"navbar": "playlist"}
    return render(request, "frontend/playlist.html", context)


def research(request):
    context = {"navbar" : "research"}
    return render(request, "frontend/research.html", context)


def research_parameters(request):
    lst = all_list()
    artist_lst = list()
    track_lst = list()
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    try:
        track = request.GET['track']
        artist = request.GET['artist']
        if track != '':
            for dic in lst:
                if track.lower() in dic['title'].lower() and artist.lower() in dic['name'].lower():
                    track_lst.append(dic)
                    artist_lst.append(dic)
            context = {"navbar": "research", "track": track_lst, "artist": artist_lst}
            return render(request, "frontend/index.html", context)
        elif track != '':
            for dic in lst:
                if track.lower() in dic['title'].lower():
                    track_lst.append(dic)
            context = {"navbar": "research", "track": track_lst, "artist": track_lst}
            return render(request, "frontend/index.html", context)
        elif artist != '':
            for dic in lst:
                if artist.lower() in dic['name'].lower():
                    artist_lst.append(dic)
            context = {"navbar": "research", "track": artist_lst, "artist": artist_lst}
            return render(request, "frontend/index.html", context)
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
