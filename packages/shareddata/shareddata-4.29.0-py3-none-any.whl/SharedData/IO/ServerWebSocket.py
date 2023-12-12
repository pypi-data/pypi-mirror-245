
import time
import sys
import time
import select
import numpy as np
import pandas as pd
import asyncio
import websockets

#TODO: DONT SERVE DATA IF TABLE IS NOT IN MEMORY
class ServerWebSocket():

    BUFF_SIZE = 32768
    RATE_LIMIT = 1e6 # 1MB/s
    # Dict to keep track of all connected client sockets
    clients = {}
    # Create a lock to protect access to the clients Dict
    lock = asyncio.Lock()
    server = None
    shdata = None
    accept_clients = None

    @staticmethod
    async def runserver(shdata, host, port):

        ServerWebSocket.shdata = shdata

        ServerWebSocket.server = await websockets.serve(ServerWebSocket.handle_client_thread, host, port)

        await ServerWebSocket.server.wait_closed()

    @staticmethod
    async def handle_client_thread(conn, path):
        addr = conn.remote_address
        Logger.log.info(f"New client connected: {addr}")
        # conn.settimeout(60.0)

        # Add the client socket to the list of connected clients
        async with ServerWebSocket.lock:
            ServerWebSocket.clients[conn] = {
                'watchdog': time.time_ns(),
                'transfer_rate': 0.0,
            }

        sockdata = ServerWebSocket.clients[conn]
        lookbacklines = 1000
        lookbackfromdate = None
        lookbackfromid = None
        transfer_rate = 0
        try:
            while True:
                try:                
                    data = await conn.recv()
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
                                sockdata['table'] = ServerWebSocket.shdata.table(
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
                                    np.floor(ServerWebSocket.BUFF_SIZE/table.itemsize))
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
                                msgmintime = msgbytes/ServerWebSocket.RATE_LIMIT
                                t = time.time_ns()
                                msg = table[ids2send[sentrows:sentrows +
                                                     msgsize]].tobytes()                                
                                conn.sendall(msg)
                                sentrows += msgsize
                                msgtime = (time.time_ns()-t)*1e-9
                                ratelimtime = max(msgmintime-msgtime,0)
                                if ratelimtime > 0:
                                    await asyncio.sleep(ratelimtime)

                            totalsize = (sentrows*table.itemsize)/1e6
                            totaltime = (time.time_ns()-tini)*1e-9
                            transfer_rate = totalsize/totaltime
                                
                            # clear watchdog
                            sockdata['watchdog'] = time.time_ns()
                            sockdata['transfer_rate'] = transfer_rate

                    await asyncio.sleep(0.0001)
                except Exception as e:
                    Logger.log.error(
                        'Client %s disconnected with error:%s' % (addr,e))
                    break
        finally:
            async with ServerWebSocket.lock:
                ServerWebSocket.clients.pop(conn)
            Logger.log.info(f"Client {addr} disconnected.")
            conn.close()

async def send_heartbeat():
    while True:
        n = 0
        sendheartbeat = True
        # Create a list of keys before entering the loop
        client_keys = list(ServerWebSocket.clients.keys())
        for client_key in client_keys:
            n = n+1
            c = ServerWebSocket.clients.get(client_key)
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
        await asyncio.sleep(15)


async def main():
    # Assuming that send_heartbeat is also an async function
    await asyncio.gather(
        ServerWebSocket.runserver(shdata, host, port),
        send_heartbeat()
    )

if __name__ == '__main__':

    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ServerWebSocket', user='master')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)
    
    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])
    
    asyncio.run(main())

    Logger.log.info('ROUTINE STARTED!')
    