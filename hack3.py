import socket
import sys

def send_pw(client_socket, pw):
    client_socket.send(pw.encode())
    response = client_socket.recv(1024)
    response = response.decode()
    return response

def build_pwv(index, pw, sendlist):
    if index == len(pw):
        sendlist.append(pw)
        return

    low = pw[index].lower()
    up = pw[index].upper()

    if index == len(pw) - 1:
        bef = pw[:len(pw) - 1]
        build_pwv(index + 1, bef + low, sendlist)
        if low != up:
            build_pwv(index + 1, bef + up, sendlist)
        return

    if index == 0:
        aft = pw[index + 1:]
        build_pwv(index + 1, low + aft, sendlist)
        if low != up:
            build_pwv(index + 1, up + aft, sendlist)
        return

    bef = pw[0:index]
    aft = pw[index + 1:]
    build_pwv(index + 1, bef + low + aft, sendlist)
    if low != up:
        build_pwv(index + 1, bef + up + aft, sendlist)

def search_pw(client_socket, pwlist):
    for pw in pwlist:
        pw = pw.strip("\n")
        sendlist = []
        build_pwv(0, pw, sendlist)
        for pwv in sendlist:
            if send_pw(client_socket, pwv) == "Connection success!":
               return pwv
   
hostname = sys.argv[1]
port = int(sys.argv[2])

file = open("passwords.txt")
pwlist = file.readlines()
file.close()

with socket.socket() as client_socket:
    address = (hostname, port)
    client_socket.connect(address)
    print(search_pw(client_socket, pwlist))
