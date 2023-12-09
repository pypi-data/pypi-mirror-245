import urllib.request
import urllib.parse
import random
import uuid
import os
def open():
    key = random.randint(0, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
    if not f"\n{str(key)}\n" in urllib.request.urlopen("http://advanced.figit.club/serverhandler/servers.txt").read().decode():
        if not f"\n{uuid.getnode()}\n" in urllib.request.urlopen("http://advanced.figit.club/serverhandler/owners.txt").read().decode():
            urllib.request.urlopen("http://advanced.figit.club/serverhandler/open.php", data=urllib.parse.urlencode({"key": key, "hwid": uuid.getnode()}).encode())
            return key
        else:
            os.system("start https://nullfr.mysellix.io/product/server-handler-1-server")
            return "You already own a server! Buy a new server to continue."
    else:
        rekey = open()
        return rekey
def receive(server):
    return urllib.request.urlopen(f"http://advanced.figit.club/serverhandler/{server}/output.txt").read().decode()
def send(server, data):
    letters = sum(letter.isalpha() for letter in data)
    if letters < 10000:
        urllib.request.urlopen("http://advanced.figit.club/serverhandler/send.php", data=urllib.parse.urlencode({"server": server, "data": data}).encode())
    else:
        print("Data too large!")
def append(server, data):
    letters = sum(letter.isalpha() for letter in urllib.request.urlopen(f"http://advanced.figit.club/serverhandler/{server}/output.txt").read().decode())+sum(letter.isalpha() for letter in data)
    if letters < 10000:
        urllib.request.urlopen("http://advanced.figit.club/serverhandler/append.php", data=urllib.parse.urlencode({"server": server, "data": data}).encode())
    else:
        print("Server cannot handle that much data! If this error continues, contact the the owner of this server.")
def clear(server):
    urllib.request.urlopen("http://advanced.figit.club/serverhandler/clear.php", data=urllib.parse.urlencode({"server": server}).encode())
def filled(server):
    letters = sum(letter.isalpha() for letter in urllib.request.urlopen(f"http://advanced.figit.club/serverhandler/{server}/output.txt").read().decode())
    if letters > 9500:
        return True
    else:
        return False
def data(server):
    return sum(letter.isalpha() for letter in urllib.request.urlopen(f"http://advanced.figit.club/serverhandler/{server}/output.txt").read().decode())