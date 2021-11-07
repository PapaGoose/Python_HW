import socket
import time


class ClientError(Exception):
    pass


class Client:

    def __init__(self, ip, port, timeout=None):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((ip, port), timeout=timeout)

    def put(self, com, data, timestamp=None):
        if not timestamp:
            response = f'put {com} {data} {int(time.time())}\n'
        else:
            response = f'put {com} {data} {int(timestamp)}\n'
        try:
            self.sock.send(response.encode('ascii'))
            if self.sock.recv(1024).decode('utf-8').split('\n')[0] != 'ok':
                raise ClientError
        except socket.error as ex:
            raise ClientError(ex)

    def get(self, key):
        x = {}
        response = f'get {key}\n'
        self.sock.send(response.encode('ascii'))
        recv = self.sock.recv(1024).decode('utf-8')

        if recv == 'ok\n\n':
            return x

        if recv.split('\n')[0] != 'ok':
            raise ClientError

        try:
            new_recv = recv[:-2].split('\n')[1:]
            keys = [str(i.split()[0]) for i in new_recv]
            floats = [float(i.split()[1]) for i in new_recv]
            integers = [int(i.split()[2]) for i in new_recv]
            tuples = [(integers[i], floats[i]) for i in range(len(integers))]
            for ind in range(len(keys)):
                if keys[ind] in x.keys():
                    x[keys[ind]].append(tuples[ind])
                else:
                    x[keys[ind]] = [tuples[ind]]
            for key, value in x.items():
                x[key] = sorted(value, key=lambda tup: tup[0])
            return x
        except socket.error as ex:
            raise ClientError(ex)
