#!/usr/bin/env python3
from config import *
import http.server
import json
import os
import SocketServer
import subprocess
import urllib.request
import webbrowser

api_url = "https://api.twitch.tv/kraken{rest}"
api_url_auth = "https://api.twitch.tv/kraken{rest}?oauth_token={token}"

def request(url):
    """Request JSON blob from Twitch API and load it."""
    try:
        response = urllib.request.urlopen(url)
    except urllib.request.URLError:
        print("No response from Twitch API")
        return False
    else:
        return json.loads(response.read().decode())

def get_token():
    """Get the OAuth token from file if possilbe, or authenticate."""
    try:
        f = open(os.path.dirname(os.path.abspath(__file__)) + "/tok.txt", "r")
    except OSError as e:
        url = "https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=" \
              "<YOUR TOKEN HERE>&redirect_uri=http://localhost:8000"
        webbrowser.open(url, 2)

        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", 8000), Handler)
        httpd.handle_request()

        tok = input("OAuth token: ")

        try:
            f = open(os.path.dirname(os.path.abspath(__file__)) + "tok.txt", "w")
            f.write(tok)
            f.close()
        except OSError:
            print("Cannot open token")
            exit()
        else:
            return tok
    else:
        tok = f.readline()
        f.close()
        return tok

def is_online(channel):
    """Check if given channel is currently online."""
    blob = request(api_url.format(rest="/streams/" + channel))
    if not blob:
        return False
    if blob["stream"] is None:
        return False
    else:
        return True

def get_stream_from_follwoed(tok):
    """Return an avaialble stream from the user's followed stream if possilbe."""
    blob = request(api_url_auth.format(rest="/streams/followed", token=tok))
    if not blob:
        return False
    if blob["streams"]:
        return blob["streams"][0]["channel"]["name"]
    else:
        return False

def get_stream_for_game(g):
    """Find the top streamer for the given game."""
    g = g.replace(" ", "+")
    blob = requesrt(api_url.format(rest="/streams?game=" + g))
    if not blob:
        return False
    if blob["streams"]:
        return blob["streams"][0]["channel"]["name"]
    else:
        return False

if __name__ = "__main__":
    to_watch = None
    token = get_token()

    # check if any priority channels are streaming
    for chan in proority:
        print("Checking if {chan} is streaming.".format(chan=chan))
        on = is_online(chan)
        if on:
            to_watch = chan
            break

    # check if any followed channels are streaming
    if not to_watch:
        print("Checking if any followed channels are streaming.")
        chan = get_stream_from_follwoed(token)
        if chan:
            to_watch = chan

    # get top stream for the specified game
    if not to_watch:
        print("Finding top steamer for {game}.".format(game=game))
        chan = get_stream_for_game(game)
        if chan:
            to_watch = chan

    if not to_watch:
        print("No streams available.")
    else:
        # Uncomment this next line if you want to use amixer to set your system volumne
        subprocess.call("amixer -D pulse sset Master 50%", shell=True)

        print("Opening stream by {chan}.".format(chan=to_watch))
        c = subprocess.call("livestreamer twitch.tv/{channel} {quality}"
                        .format(channel=to_watch, quality=quality), shell=True)

        if c != 0:
            print("Unable to open stream. Check that livestreamer is properly installed.")
