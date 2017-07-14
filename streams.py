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
            