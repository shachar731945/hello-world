"""
this class is a client which is used to communicate between the server and this 
client it uses socket to communice between it and the server, to close and open
connection and to send and receive messages
"""

import socket
import select

IP_CONNECTION = '127.0.0.1'
PORT_CONNECTION = 8820
RECV_LENGTH_DEFAULT = 1024


class SocketClient:

    def __init__(self):
        """
        this function creates an instance of this class, intializes and 
        conencting the socket to the server of the chat
        """
        self._client_socket = socket.socket()
        self._client_socket.connect((IP_CONNECTION, PORT_CONNECTION))
        self._wlist = []

    def read_message(self):
        """
        this function uses the module select to check if there was a message was
        sent to the client to be received and keeps the wlist, the list of 
        socket that can be written afterwards (the client socket)
        :return: the message that was received to the the socket, an empty 
        string if nothing was received
        """
        rlist, wlist, xlist = select.select(
            [self._client_socket], [self._client_socket], [])
        self._wlist = wlist
        if rlist:
            message = self.recv_message()
            return message
        return ''

    def recv_message(self):
        """
        this function returns the message that the socket received
        :return: the message itself that was received
        """
        message = self._client_socket.recv(RECV_LENGTH_DEFAULT)
        return message

    def close_connection(self):
        """
        this fucntion closes connection with the server, closes the socket between them
        :return: 
        """
        self._client_socket.close()

    def send_message(self, message):
        """
        this fucntion sends a message from this client_socket to the server
        socket, if it exist if wlist, can be written to
        :param message: the message to be sent
        :return: 
        """
        if self._client_socket in self._wlist:
            self._client_socket.send(message)
