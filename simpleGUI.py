# img_viewer.py

import PySimpleGUI as sg
import UDP_Sender
import threading
import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

ip_Addr = local_ip   # Must set ip of PC
port = 4550  # Same port declared in sender
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip_Addr, port)
opened_socket.bind(server_address)


def the_thread(window):
    while True:
        data, addr = opened_socket.recvfrom(1024)
        #print(data)
        window.write_event_value('-THREAD-', data)


# First the window layout in 2 columns

_column = [
    [
        sg.Text("IP Address",size=(15, 1)),
        sg.In(size=(25, 1), key="-IP-"),
    ],
    [
        sg.Text("Message to send",size=(15, 1)),
        sg.In(size=(25, 1), key="-MSGSENT-"),
        sg.Button('Send')
    ],
    [
        sg.HorizontalSeparator(),
    ],
    [
        sg.Text("Message Received", size=(15, 1)),
        sg.In(size=(25, 1), key="-MSGRECV-"),
    ]
]


layout = [
    [
        sg.Column(_column),
    ]
]


window = sg.Window("Packet Sender/Receiver", layout)

threading.Thread(target=the_thread, args=(window,), daemon=True).start()

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    #
    if event == "-THREAD-":
        data = values[event]
        window["-MSGRECV-"].update(data.decode('utf-8'))

    if event == "Send":
        ipAdd = values["-IP-"]
        cmd = values["-MSGSENT-"]
        UDP_Sender.udpSender(cmd, ipAdd,4550)


window.close()

