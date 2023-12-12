
import time
import sys
import socket
import threading
import time
import select
import numpy as np
import pandas as pd

#TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY
class ServerSocket():

    BUFF_SIZE = 32768
    RATE_LIMIT = 1e6 # 1MB/s
    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = threading.Lock()
    server = None
    shdata = None
    accept_clients = None

    @staticmethod
    def runserver(shdata, host, port):

        ServerSocket.shdata = shdata

        ServerSocket.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # This line allows the address to be reused
        ServerSocket.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Create the server and start accepting clients in a new thread
        ServerSocket.accept_clients = threading.Thread(
            target=ServerSocket.accept_clients_thread, args=(host, port))
        ServerSocket.accept_clients.start()

    @staticmethod
    def accept_clients_thread(host, port):
        ServerSocket.server.bind((host, port))
        ServerSocket.server.listen()

        Logger.log.info(f'Listening on {host}:{port}')

        while True:
            conn, addr = ServerSocket.server.accept()
            threading.Thread(target=ServerSocket.handle_client_thread,
                             args=(conn, addr)).start()

    @staticmethod
    def handle_client_thread(conn, addr):
        Logger.log.info(f"New client connected: {addr}")
        conn.settimeout(60.0)

        # Add the client socket to the list of connected clients
        with ServerSocket.lock:
            ServerSocket.clients[conn] = {
                'watchdog': time.time_ns(),
                'transfer_rate': 0.0,
            }

        sockdata = ServerSocket.clients[conn]
        lookbacklines = 1000
        lookbackfromdate = None
        lookbackfromid = None
        transfer_rate = 0
        try:
            while True:
                try:
                    # Check if there is data ready to be read from the client
                    ready_to_read, _, _ = select.select([conn], [], [], 0)
                    if ready_to_read:
                        # Receive data from the client
                        data = conn.recv(ServerSocket.BUFF_SIZE)
                        if data:
                            # clear watchdog
                            sockdata['watchdog'] = time.time_ns()
                            data = data.decode()
                            msg = data.split('#')[1].split(',')
                            msgtype = msg[0]
                            if msgtype == 'subscribe':
                                database = msg[1]
                                period = msg[2]
                                source = msg[3]
                                container = msg[4]
                                if container == 'table':
                                    tablename = msg[5]
                                    Logger.log.info('Serving updates of %s/%s/%s/%s' %
                                                    (database, period, source, tablename))
                                    sockdata['table'] = ServerSocket.shdata.table(
                                        database, period, source, tablename)
                                    sockdata['count'] = int(msg[6])
                                    timestamp = float(msg[7])
                                    datetime_ns = np.datetime64(
                                        int(timestamp), 's')
                                    datetime_ns += np.timedelta64(
                                        int((timestamp % 1)*1e9), 'ns')
                                    sockdata['mtime'] = datetime_ns
                                    table = sockdata['table']
                                    sockdata['maxrows'] = int(
                                        np.floor(ServerSocket.BUFF_SIZE/table.itemsize))
                                    if len(msg) > 8:
                                        lookbacklines = int(msg[8])
                                    if len(msg) > 9:
                                        lookbackfromdate = pd.Timestamp(msg[9])
                                        lookbackfromid,_ = table.get_date_loc(lookbackfromdate)
                                        if lookbackfromid == -1:
                                            lookbackfromid = table.count

                        else:
                            break

                    if 'table' in sockdata:
                        table = sockdata['table']
                        ids2send = []

                        lastmtime = sockdata['mtime']
                        if lookbackfromid is not None:
                            lookbackid = lookbackfromid
                        else:
                            lookbackid = table.count-lookbacklines
                        if lookbackid < 0:
                            lookbackid = 0
                        updtids = np.where(
                            table[lookbackid:]['mtime'] > lastmtime)
                        if len(updtids) > 0:
                            ids2send.extend(updtids[0]+lookbackid)
                            sockdata['mtime'] = max(
                                table[lookbackid:]['mtime'])

                        lastcount = sockdata['count']
                        curcount = table.count.copy()
                        if curcount > lastcount:
                            newids = np.arange(lastcount, curcount)
                            ids2send.extend(newids)
                            sockdata['count'] = curcount

                        if len(ids2send) > 0:
                            ids2send = np.unique(ids2send)
                            ids2send = np.sort(ids2send)
                            maxrows = sockdata['maxrows']
                            rows2send = len(ids2send)
                            sentrows = 0                            
                            tini = time.time_ns()
                            while sentrows < rows2send:                                
                                msgsize = min(maxrows, rows2send)
                                msgbytes = msgsize*table.itemsize
                                msgmintime = msgbytes/ServerSocket.RATE_LIMIT
                                t = time.time_ns()
                                msg = table[ids2send[sentrows:sentrows +
                                                     msgsize]].tobytes()                                
                                conn.sendall(msg)
                                sentrows += msgsize
                                msgtime = (time.time_ns()-t)*1e-9
                                ratelimtime = max(msgmintime-msgtime,0)
                                if ratelimtime > 0:
                                    time.sleep(ratelimtime)

                            totalsize = (sentrows*table.itemsize)/1e6
                            totaltime = (time.time_ns()-tini)*1e-9
                            transfer_rate = totalsize/totaltime
                                
                            # clear watchdog
                            sockdata['watchdog'] = time.time_ns()
                            sockdata['transfer_rate'] = transfer_rate

                    time.sleep(0.0001)
                except Exception as e:
                    Logger.log.error(
                        'Client %s disconnected with error:%s' % (addr,e))
                    break
        finally:
            with ServerSocket.lock:
                ServerSocket.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()


if __name__ == '__main__':

    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerSocket', user='master')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)

    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])
    ServerSocket.runserver(shdata, host, port)

    Logger.log.info('ROUTINE STARTED!')
    while True:
        n = 0
        sendheartbeat = True
        # Create a list of keys before entering the loop
        client_keys = list(ServerSocket.clients.keys())
        for client_key in client_keys:
            n = n+1
            c = ServerSocket.clients.get(client_key)
            if c is not None:
                if 'table' in c:
                    table = c['table'].table
                    tf = c['transfer_rate']
                    Logger.log.debug('#heartbeat#%.2fMB/s,%i:%s,%s' %
                                    (tf,n, client_key.getpeername(), table.relpath))
                else:            
                    Logger.log.debug('#heartbeat# %i:%s' %
                                    (n, client_key.getpeername()))
                sendheartbeat = False
        if sendheartbeat:
            Logger.log.debug('#heartbeat#host:%s,port:%i' % (host, port))
        time.sleep(15)