import time
import sys
import socket
import threading
import time
import select
import numpy as np
import pandas as pd

from SharedData.Logger import Logger
from SharedData.IO.ServerSocket import ServerSocket

class ClientSocket():
    @staticmethod
    def table_subscribe_thread(table, host, port, lookbacklines=1000, lookbackdate=None):

        shnumpy = table.records
        buffsize = int(np.floor(ServerSocket.BUFF_SIZE/shnumpy.itemsize))*shnumpy.itemsize
        bytes_buffer = bytearray()

        while True:
            try:
                client_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                if lookbackdate is None:
                    msg = '#subscribe,%s,%s,%s,table,%s,%i,%.6f,%i#' % \
                        (table.database, table.period, table.source,
                        table.tablename, int(shnumpy.count), float(shnumpy.mtime), lookbacklines)
                elif isinstance(lookbackdate, pd.Timestamp):
                    msg = '#subscribe,%s,%s,%s,table,%s,%i,%.6f,%i,%s#' % \
                        (table.database, table.period, table.source,
                        table.tablename, int(shnumpy.count), float(shnumpy.mtime), lookbacklines,lookbackdate.strftime('%Y-%m-%d'))
                msgb = msg.encode('utf-8')
                data = client_socket.send(msgb)
                while True:
                    try:
                        # Receive data from the server
                        data = client_socket.recv(buffsize)
                        if data == b'':
                            msg = 'Subscription %s,%s,%s,table,%s closed !' % \
                                (table.database, table.period,
                                 table.source, table.tablename)
                            Logger.log.warning(msg)
                            client_socket.close()
                        else:
                            bytes_buffer.extend(data)

                            if len(bytes_buffer) >= shnumpy.itemsize:
                                # Determine how many complete records are in the buffer
                                num_records = len(
                                    bytes_buffer) // shnumpy.itemsize
                                # Take the first num_records worth of bytes
                                record_data = bytes_buffer[:num_records *
                                                           shnumpy.itemsize]
                                # And remove them from the buffer
                                del bytes_buffer[:num_records *
                                                 shnumpy.itemsize]
                                # Convert the bytes to a NumPy array of records
                                rec = np.frombuffer(
                                    record_data, dtype=shnumpy.dtype)
                                # Upsert all records at once
                                shnumpy.upsert(rec)

                    except Exception as e:
                        msg = 'Subscription %s,%s,%s,table,%s error!\n%s' % \
                            (table.database, table.period,
                             table.source, table.tablename, str(e))
                        Logger.log.error(msg)
                        client_socket.close()
                        break
            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(5)
