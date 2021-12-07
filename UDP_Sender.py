import socket

opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def udpSender(command, ip_Addr, port):
    byte_message = bytes(command, "utf-8")
    opened_socket.sendto(byte_message, (ip_Addr, port))

