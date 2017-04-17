"""
this class is a server which is used to sommunice between it and the other 
clients, opening and closing connections with them, sending and receiving 
messages from them
"""
import socket
import select

RECV_LENGTH_DEFAULT = 1024
PORT = 8820
LISTEN_TO_ALL_IP = '0.0.0.0'
NUM_OF_PEOPLE_TO_LISTEN = 5


class SocketServer:

    def __init__(self):
        """
        this function creates an instance of this class, intializes the server 
        socket so it can create connections later
        """
        self._server_socket = socket.socket()
        self._server_socket.bind((LISTEN_TO_ALL_IP, PORT))
        self._server_socket.listen(NUM_OF_PEOPLE_TO_LISTEN)
        self._client_sockets = []
        self._wlist = []

    def read_messages_requests(self):
        """
        this function uses the module select to check if there was a messages 
        and requests was sent to the client to be received and keeps the wlist,
        the list of socket that can be written afterwards (the client socket)
        :return: the fucntion handle requests with all the requests that the 
        server and it's connections received
        """
        rlist, wlist, xlist = select.select(
            self._client_sockets + [self._server_socket],
            self._client_sockets, [])
        self._wlist = wlist
        return self.handle_requests(rlist)

    def handle_requests(self, rlist):
        """
        this function gets the list of all the requests and seperating them to 
        new connection request and messages from existing client sockets and 
        returns them for future use
        :param rlist: a list of all the requests that the server got
        :return: the new client_socket of the new user if there is and the 
        messages form the existing client_sockets
        """
        new_user = None
        client_requests = []
        for request_socket in rlist:
            if request_socket is self._server_socket:
                new_user = self.accpet_client_socket()
            else:
                client_requests.append(SocketServer.read_from_client(
                    request_socket))
        return new_user, client_requests

    @staticmethod
    def read_from_client(client_socket):
        """
        this message returns a message that is received by a client socket
        :param client_socket: the client socket to read the message from
        :return: the message itself
        """
        message = SocketServer.recv_message(client_socket)
        return client_socket, message

    def accpet_client_socket(self):
        """
        this function connects to the server to another client, accepting 
        another client_socket and creates it, it updates the attributes of the
        class about it
        :return: the new socket
        """
        (new_socket, address) = self._server_socket.accept()
        self._client_sockets.append(new_socket)
        return new_socket

    @staticmethod
    def recv_message(request_socket):
        """
        a duplication of read_from_client method
        """
        return request_socket.recv(RECV_LENGTH_DEFAULT)

    def send_specific_message(self, client_socket, message):
        """
        this function sends to a specific socket a message from the server
        :param client_socket: the socket to send to
        :param message: the message to send
        :return: 
        """
        for to_send_socket in self._wlist:
            if client_socket == to_send_socket:
                client_socket.send(message)

    def send_message_to_others(self, client_socket, message):
        """
        this function sends a message to every socket that it is possible to 
        send to (in the wlist) exept the socket which one of the params of the
        function
        :param client_socket: the socket not to send to
        :param message: the message itself
        :return: 
        """
        print message
        for to_send_socket in self._wlist:
            if to_send_socket != client_socket:
                to_send_socket.send(message)

    def remove_socket(self, client_socket):
        """
        this fucntion removes a certain socket from the classes attributes after 
        the connection with hom got closed for future use
        :param client_socket: the socket which is close and need to be removed 
        :return: 
        """
        client_socket.close()
        self._client_sockets.remove(client_socket)

    def send_message_to_all(self, message):
        """
        this function sends a message to every socket that it is possible to 
        send to (in the wlist)
        :param message: the message to send
        :return: 
        """
        for to_send_socket in self._client_sockets:
            to_send_socket.send(message)
